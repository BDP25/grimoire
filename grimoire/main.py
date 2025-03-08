import typer

from grimoire import __version__
from grimoire.add import add_cli
from grimoire.ask import ask_cli
from grimoire.init import init_cli
from grimoire.sync import sync_cli
from grimoire.verify import verify_cli

CLI_NAME = "grimoire"
DESCRIPTION = """
A cli which enables RAG for your project 🔮
"""

cli = typer.Typer(
    name=CLI_NAME,
    help=DESCRIPTION,
    add_completion=False,
)

cli.add_typer(ask_cli, name=None)
cli.add_typer(sync_cli, name=None)
cli.add_typer(verify_cli, name=None)
cli.add_typer(add_cli, name=None)
cli.add_typer(init_cli, name=None)


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@cli.command()
def version() -> None:
    typer.echo(f"grim cli v{__version__}")
