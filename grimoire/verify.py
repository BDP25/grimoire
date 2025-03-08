import os

import typer

from grimoire.configuration import ProjectConfiguration

verify_cli = typer.Typer()


@verify_cli.command("verify", help="Verify the configuration of the project")
def verify() -> None:
    if not os.path.exists("grimoire.yaml"):
        typer.echo("No configuration file found. Please run `grim init` first.")
        raise typer.Exit(code=1)
    typer.echo("Verifying configuration")
    config = ProjectConfiguration.load_from_yaml()
    prefix = typer.style("Successful for", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"{prefix}: {config.name}")
