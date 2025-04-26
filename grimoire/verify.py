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
    path: Path = typer.Argument(  # noqa: B008
        get_recursive_config(),  # noqa: B008
        help="Path to the grimoire project",
    ),
) -> None:
    """
    Verify the configuration of the project.

    :param path: Path to the grimoire project.
    """
    if not (path / CONFIG_FILE_NAME).exists():
        typer.echo("No configuration file found. Please run `grim init` first.")
        raise typer.Exit(code=1)
    typer.echo("Verifying configuration")
    config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)
    typer.echo(f"{green_text('Successful for')}: {config.name}")
