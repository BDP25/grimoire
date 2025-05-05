from pathlib import Path

import typer

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
    get_recursive_config,
)
from grimoire.helpers.typer import green_text

verify_cli = typer.Typer()


@verify_cli.command("verify", help="Verify the configuration of the project")
def verify(
    path: Path | None = typer.Option(  # noqa: B008
        None, "--path", help="Path to the grimoire project"
    ),
) -> None:
    """
    Verify the configuration of the project.

    :param path: Path to the grimoire project.
    """
    if path is None:
        path = get_recursive_config()

    if not (path / CONFIG_FILE_NAME).exists():
        typer.echo("No configuration file found. Please run `grim init` first.")
        raise typer.Exit(code=1)

    typer.echo("Verifying configuration")
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)
    typer.echo(f"{green_text('Successful for')}: {config.name}")
