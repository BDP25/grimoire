from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

import psycopg
import typer
from git import Repo
from langchain_postgres import PGVector
from rich.progress import track

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
    get_recursive_config,
)
from grimoire.helpers.ingestion import code_ingestion, text_ingestion
from grimoire.helpers.vectorstore import (
    clear_collection,
    setup_vectorstore,
    vectorstore_connection,
)

DEFAULT_EXCLUDE = [".git", ".venv", ".env", "sandbox"]
sync_cli = typer.Typer()


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

    typer.echo("Syncing grimoire project")
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

    if not config.sources:
        typer.echo("No sources found in configuration file")
        raise typer.Abort()

    try:
        connection = vectorstore_connection(config.db)
        clear_collection(config.llm.collection, connection)
    except psycopg.OperationalError as e:
        typer.echo("Error connecting to the database")
        raise e

    text_splits = []
    code_splits = []

    if config.include_project:
        text_splits += text_ingestion(path, config.llm, exclude=DEFAULT_EXCLUDE)
        code_splits += code_ingestion(
            path, config.llm, glob=f"{config.project_src}/**/*"
        )

    for repo in track(config.sources, description="Processing sources"):
        if not repo.include_md and not repo.include_code:
            continue

        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            Repo.clone_from(repo.url, to_path=temp_path)

            if repo.include_md:
                text_splits += text_ingestion(temp_path, config.llm)

            if repo.include_code:
                code_splits += code_ingestion(temp_path, config.llm)

    if text_splits or code_splits:
        vectorstore = setup_vectorstore(config.llm.collection, connection)
        vectorstore = cast(PGVector, vectorstore)  # hack to avoid mypy error

        if text_splits:
            vectorstore.add_documents(text_splits, metadata={"source": "text"})

        if code_splits:
            vectorstore.add_documents(code_splits, metadata={"source": "code"})
