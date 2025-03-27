from pathlib import Path

import typer

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    CodeSource,
    DBConfiguration,
    DocumentSource,
    LLMConfiguration,
    ProjectConfiguration,
)

init_cli = typer.Typer()

DUMMY_DOCS = [
    DocumentSource(url="https://github.com/numpy/numpy"),
    DocumentSource(url="https://github.com/pandas-dev/pandas"),
]

DUMMY_CODE = [
    CodeSource(url="https://github.com/pandas-dev/pandas"),
]


def get_project_config(path: Path) -> ProjectConfiguration:
    """
    Queries user input and returns full project configuration

    :param path: Path where configuration will be saved
    :return: ProjectConfiguration
    """
    project_name = typer.prompt("Project name", default=path.name)

    db_config = DBConfiguration(
        host=typer.prompt("Database host", default="localhost"),
        port=typer.prompt("Database port", default="5432"),
        user=typer.prompt("Database user", default="pgvector"),
        password=typer.prompt("Database password", default="pgvector"),
    )

    collection = typer.prompt("Unique collection name", default=path.name)
    if typer.confirm("Want to modify default chunk size and overlapp?", default=False):
        ingestion_config = LLMConfiguration(
            collection=collection,
            text_chunk_size=typer.prompt("Text chunk size", default=512, type=int),
            text_chunk_overlap=typer.prompt(
                "Text chunk overlap", default=128, type=int
            ),
            code_chunk_size=typer.prompt("Code chunk size", default=512, type=int),
            code_chunk_overlap=typer.prompt(
                "Code chunk overlap", default=128, type=int
            ),
        )
    else:
        ingestion_config = LLMConfiguration(
            collection=collection,
            text_chunk_size=512,
            text_chunk_overlap=128,
            code_chunk_size=512,
            code_chunk_overlap=128,
        )

    return ProjectConfiguration(
        name=project_name,
        llm=ingestion_config,
        db=db_config,
        docs=DUMMY_DOCS,
        code=DUMMY_CODE,
    )


@init_cli.command("init", help="Initialize a new grimoire project")
def init(
    path: Path = typer.Argument(  # noqa: B008
        Path.cwd(),  # noqa: B008
        help="Path where grimoire project should be created",
    ),
) -> None:
    file_path = path / CONFIG_FILE_NAME

    if not path.is_dir():
        typer.echo(f"Error: Path {path} does not exist", err=True)
        raise typer.Exit(code=1)
    if file_path.exists() and not typer.confirm(
        f"File {file_path} already exists. Overwrite?"
    ):
        typer.echo("Exiting without overwriting existing file")
        raise typer.Exit(code=0)

    config: ProjectConfiguration = get_project_config(path)
    config.save_to_yaml(file_path)
    typer.echo(f"Configuration saved at {file_path}")
