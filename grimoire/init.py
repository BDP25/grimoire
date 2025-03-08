import typer

init_cli = typer.Typer()


@init_cli.command("init", help="Initialize a new grimoire project")
def init() -> None:
    typer.echo("Initializing new grimoire project")
