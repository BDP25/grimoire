import typer

add_cli = typer.Typer()


@add_cli.command("add", help="Add a new dependency or document to the project")
def add() -> None:
    typer.echo("Adding new spell")
