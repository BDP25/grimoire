import os
from pathlib import Path
from typing import cast

import typer
from langchain_postgres import PGVector

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    ProjectConfiguration,
    get_recursive_config,
)
from grimoire.helpers.llm import setup_llm
from grimoire.helpers.retriever import get_retrieval_chain
from grimoire.helpers.typer import red_text
from grimoire.helpers.vectorstore import setup_vectorstore, vectorstore_connection

ask_cli = typer.Typer()


@ask_cli.command("ask", help="Ask a question with project context")
def ask(
    question: list[str],
    skip_rag: bool = typer.Option(False, "--skip-rag", help="Skip the RAG process"),
    path: Path = typer.Option(  # noqa: B008
        get_recursive_config(),  # noqa: B008
        "--path",
        help="Path to the grimoire project",
    ),
) -> None:
    """
    Ask a question either with or without the RAG process (--skip-rag flag).

    :param question: Question as a list of words.
    :param skip_rag: Flag to skip the RAG process and use only the LLM.
    :param path: Path to the grimoire project.
    """
    if not os.getenv("LLM_API_KEY"):
        typer.echo("LLM_API_KEY environment variable is not set.")
        raise typer.Abort()

    typer.echo(f"{red_text('Grimoire 🔮: ')}")
    question_str = " ".join(question)

    llm = setup_llm()

    if skip_rag:
        for chunk in llm.stream(question_str):
            typer.echo(chunk.content, nl=False)

    else:
        config = ProjectConfiguration.load_from_yaml(path / CONFIG_FILE_NAME)

        connection = vectorstore_connection(config.db)
        vectorstore = setup_vectorstore(config.llm.collection, connection)
        vectorstore = cast(PGVector, vectorstore)

        rag_client = get_retrieval_chain(vectorstore, llm, config.llm)

        for chunk in rag_client.stream(question_str):
            typer.echo(chunk, nl=False)
