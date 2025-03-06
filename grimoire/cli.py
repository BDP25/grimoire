import os

import typer
from google import genai
from typer.main import get_command

CLI_NAME = "grimoire"

cli = typer.Typer(
    name=CLI_NAME,
    help="A cli which enables RAG for your code 🔮",
    add_completion=False,
)


@cli.command()
def init() -> None:
    """
    Initialize a new grimoire project.
    """
    typer.echo("Initializing new grimoire project")


@cli.command()
def add() -> None:
    """
    Add a new dependency or document to the project
    """
    typer.echo("Adding new spell")


@cli.command()
def sync() -> None:
    """
    Sync the grimoire project with existing configuration
    """
    typer.echo("Syncing grimoire project")


@cli.command()
def ask(question: list[str]) -> None:
    """
    Ask a question to the grimoire
    """
    question_prefix = typer.style("Question", fg=typer.colors.BLUE, bold=True)
    answer_prefix = typer.style("Answer", fg=typer.colors.RED, bold=True)
    typer.echo(f"{question_prefix}: {' '.join(question)}")

    client = genai.Client(api_key=os.getenv("LLM_API_KEY"))
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=question,
    )
    typer.echo(f"{answer_prefix}: ", nl=False)
    for chunk in response:
        typer.echo(chunk.text, nl=False)


@cli.command("help", help="Show this message and exit")
def help_command() -> None:
    ctx = get_command(cli).make_context("grimoire", [])
    get_command(cli).get_help(ctx)


@cli.command(help="Show version and exit")
def version() -> None:
    typer.echo("0.1.0")
