import typer

from grimoire import __version__
from grimoire.ask import ask_cli
from grimoire.flush import flush_cli
from grimoire.init import init_cli
from grimoire.sync import sync_cli
from grimoire.verify import verify_cli

CLI_NAME = "grimoire"
DESCRIPTION = """
A cli which enables RAG for your project 🔮

Prequsites:\n
- Get an LLM API token (e.g. from https://aistudio.google.com/app/apikey)\n
- Set the LLM_API_TOKEN environment variable to the token\n
"""

cli = typer.Typer(
    name=CLI_NAME,
    help=DESCRIPTION,
    add_completion=False,
)

cli.add_typer(ask_cli, name=None)
cli.add_typer(flush_cli, name=None)
cli.add_typer(init_cli, name=None)
cli.add_typer(sync_cli, name=None)
cli.add_typer(verify_cli, name=None)


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
) -> None:
    """
    Gets called when no subcommand is provided and displays the help message.

    :param ctx: Typer context.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@cli.command("version", help="Print the version of the grim cli")
def version() -> None:
    """
    Print the version of the grim cli.
    """
    typer.echo(f"grim cli v{__version__}")
