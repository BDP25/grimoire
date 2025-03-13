import os
from pathlib import Path

import typer

from grimoire.configuration import CONFIG_FILE_NAME, ProjectConfiguration

verify_cli = typer.Typer()


@verify_cli.command("verify", help="Verify the configuration of the project")
def verify() -> None:
    # TODO: add dynamic path with checks see init.py
    if not os.path.exists("grimoire.yaml"):
        typer.echo("No configuration file found. Please run `grim init` first.")
        raise typer.Exit(code=1)
    typer.echo("Verifying configuration")
    config = ProjectConfiguration.load_from_yaml(Path.cwd() / CONFIG_FILE_NAME)
    prefix = typer.style("Successful for", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"{prefix}: {config.name}")
