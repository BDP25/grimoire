import os
from pathlib import Path

import typer
from langchain.chat_models.base import BaseChatModel

from grimoire.configuration import CONFIG_FILE_NAME, ProjectConfiguration
from grimoire.helpers.rag import get_retrieval_chain, setup_llm, vectorstore_connection
from grimoire.helpers.typer import red_text

ask_cli = typer.Typer()


def get_llm_client() -> BaseChatModel:
    """
    Configures a chat model client with the api key

    :return: defined chat model client
    """
    if not os.getenv("LLM_API_KEY"):
        typer.echo("LLM_API_KEY environment variable is not set.")
        raise typer.Abort()

    # TODO: add configuration options for other models, temperature, etc.
    return setup_llm()


@ask_cli.command("ask", help="Ask a question with project context")
def ask(
    question: list[str],
    skip_rag: bool = typer.Option(False, "--skip-rag", help="Skip the RAG process"),
    path: Path = typer.Option(  # noqa: B008
        Path.cwd(),  # noqa: B008
        "--path",
        help="Path to the grimoire project",
    ),
) -> None:
    typer.echo(f"{red_text('Grimoire 🔮: ')}", nl=False)
    question_str = " ".join(question)

    if skip_rag:
        client = get_llm_client()
        response = client.stream(question_str)
        for chunk in response:
            typer.echo(chunk.content, nl=False)

    else:
        # TODO: add dependency injection
        config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)
        connection = vectorstore_connection(config.db)
        rag_client = get_retrieval_chain(config.name, connection)

        response = rag_client.stream(question_str)
        for chunk in response:
            if chunk is not None:
                typer.echo(chunk, nl=False)
