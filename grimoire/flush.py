from pathlib import Path

import psycopg
import typer

from grimoire.configuration import CONFIG_FILE_NAME, ProjectConfiguration
from grimoire.helpers.rag import delete_vectorstore, vectorstore_connection

flush_cli = typer.Typer()


@flush_cli.command("flush", help="Flush the whole vectorstore")
def flush(
    path: Path = typer.Argument(  # noqa: B008
        Path.cwd(),  # noqa: B008
        help="Path to the grimoire project",
    ),
) -> None:
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

    if typer.confirm("Do you really want to flush the vectorstore?", default=False):
        try:
            vectorstore = vectorstore_connection(config.db)
            delete_vectorstore(vectorstore)
        except psycopg.OperationalError as e:
            typer.echo(f"Error: {e}")
            raise e
        typer.echo("Vectorstore flushed")
