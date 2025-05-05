from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

import psycopg
import typer
from git import Repo
from langchain_core.documents import Document
from langchain_postgres import PGVector
from rich.progress import track

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
    get_recursive_config,
)
from grimoire.helpers.ingestion import code_ingestion, text_ingestion
from grimoire.helpers.typer import green_text
from grimoire.helpers.vectorstore import (
    clear_collection,
    setup_vectorstore,
    vectorstore_connection,
)

DEFAULT_EXCLUDE = [".git", ".venv", ".env", "sandbox"]
sync_cli = typer.Typer()


def ingest_documents_to_vectorstore(
    text_splits: list[Document],
    code_splits: list[Document],
    vectorstore: PGVector,
) -> None:
    """
    Ingests documents into the vectorstore.

    :param text_splits: List of text Document objects.
    :param code_splits: List of code Document objects.
    :param vectorstore: The vectorstore instance to ingest documents into.
    """

    if text_splits:
        vectorstore.add_documents(text_splits, metadata={"source": "text"})
    if code_splits:
        vectorstore.add_documents(code_splits, metadata={"source": "code"})


@sync_cli.command("sync", help="Sync the grimoire project with existing configuration")
def sync(
    path: Path | None = typer.Option(  # noqa: B008
        None, "--path", help="Path to the grimoire project"
    ),
) -> None:
    """
    Sync the grimoire project with existing configuration and sources.

    :param path: Path to the grimoire project.
    """
    if path is None:
        path = get_recursive_config()

    if not typer.confirm(
        f"Are you sure you want to sync the grimoire project at {path}?",
        default=False,
    ):
        raise typer.Abort()

    typer.echo("Syncing grimoire project:")
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

    if not config.sources:
        typer.echo("No sources found in configuration file")
        raise typer.Abort()

    try:
        typer.echo("- Flushing vectorstore")
        connection = vectorstore_connection(config.db)
        clear_collection(config.llm.collection, connection)
    except psycopg.OperationalError as e:
        typer.echo("Error connecting to the database")
        raise e

    vectorstore = setup_vectorstore(config.llm.collection, connection)
    vectorstore = cast(PGVector, vectorstore)  # hack to avoid mypy error

    if config.include_project:
        typer.echo("- Ingesting project source code")
        text_splits = text_ingestion(path, config.llm, exclude=DEFAULT_EXCLUDE)
        code_splits = code_ingestion(
            path, config.llm, glob=f"{config.project_src}/**/*"
        )
        ingest_documents_to_vectorstore(text_splits, code_splits, vectorstore)

    typer.echo("- Ingesting sources")
    for repo in track(config.sources, description="Processing sources..."):
        if not repo.include_md and not repo.include_code:
            continue

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            source = Repo.clone_from(repo.url, to_path=temp_path)
            if repo.branch:
                source.git.checkout(repo.branch)

            if repo.include_md:
                text_splits = text_ingestion(temp_path, config.llm)

            if repo.include_code:
                code_splits = code_ingestion(temp_path, config.llm)

            ingest_documents_to_vectorstore(text_splits, code_splits, vectorstore)

    typer.echo(green_text("Sync completed! Happy wizarding! ✨"))
