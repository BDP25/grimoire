from pathlib import Path
from tempfile import TemporaryDirectory

import typer
from git import Repo
from rich.progress import track

from grimoire.configuration import CONFIG_FILE_NAME, ProjectConfiguration
from grimoire.helpers.rag import text_ingestion

sync_cli = typer.Typer()


@sync_cli.command("sync", help="Sync the grimoire project with existing configuration")
def sync(
    path: Path = typer.Argument(  # noqa: B008
        Path.cwd(),  # noqa: B008
        help="Path to the grimoire project",
    ),
) -> None:
    typer.echo("Syncing grimoire project")
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

    if not config.sources:
        typer.echo("No sources found in configuration file")
        raise typer.Exit()

    for repo in track(config.sources, description="Processing ..."):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            Repo.clone_from(repo.url, to_path=temp_path)
            text_ingestion(
                config.llm.collection,
                config.llm.text_chunk_size,
                config.llm.text_chunk_overlap,
            )
