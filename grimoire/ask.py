import os

import typer
from langchain.chat_models.base import BaseChatModel

from grimoire.helpers.rag import setup_llm
from grimoire.helpers.typer import blue_text, red_text

ask_cli = typer.Typer()


def get_llm_client() -> BaseChatModel:
    """
    Configures a chat model client with the api key

    :return: defined chat model client
    """
    if not os.getenv("LLM_API_KEY"):
        typer.echo("LLM_API_KEY environment variable is not set.")
        raise typer.Exit(code=1)

    # TODO: add configuration options for other models and options for model temperature, etc.
    return setup_llm()


@ask_cli.command("ask", help="Ask a question with project context")
def ask(question: list[str]) -> None:
    typer.echo(f"{blue_text('Question: ')}{' '.join(question)}")

    client = get_llm_client()
    response = client.stream(" ".join(question))
    typer.echo(f"{red_text('Answer: ')}", nl=False)
    for chunk in response:
        typer.echo(chunk.content, nl=False)
