import typer

sync_cli = typer.Typer()


@sync_cli.command("sync", help="Sync the grimoire project with existing configuration")
def sync() -> None:
    typer.echo("Syncing grimoire project")
