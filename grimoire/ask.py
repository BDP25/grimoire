import os

import typer
from google import genai

ask_cli = typer.Typer()


def verify_api_key() -> None:
    if not os.getenv("LLM_API_KEY"):
        typer.echo("LLM_API_KEY environment variable is not set.")
        raise typer.Exit(code=1)


@ask_cli.command("ask", help="Ask a question with project context")
def ask(question: list[str]) -> None:
    verify_api_key()

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
