from pathlib import Path

import typer

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    DBConfiguration,
    LLMConfiguration,
    ProjectConfiguration,
    Source,
)
from grimoire.helpers.typer import green_text

init_cli = typer.Typer()

DUMMY_SOURCES = [
    Source(url="https://github.com/pallets/flask"),
    Source(url="https://github.com/corydolphin/flask-cors"),
    Source(url="https://github.com/pallets-eco/flask-sqlalchemy"),
    Source(url="https://github.com/miguelgrinberg/Flask-Migrate"),
    Source(url="https://github.com/psf/requests"),
    Source(url="https://github.com/benoitc/gunicorn"),
]


def get_project_config(path: Path) -> ProjectConfiguration:
    """
    Queries user input and returns full project configuration

    :param path: Path where configuration will be saved
    :return: ProjectConfiguration
    """
    project_name = typer.prompt("Project name", default=path.name)
    include_project = typer.confirm("Include project in embeddings?", default=True)
    project_src = typer.prompt(
        "What is the project src folder? (e.g. src, <project-name>)", default=path.name
    )

    db_config = DBConfiguration(
        host=typer.prompt("Database host", default="localhost"),
        port=typer.prompt("Database port", default="5432"),
        db=typer.prompt("Database name", default="postgres"),
        user=typer.prompt("Database user", default="pgvector"),
        password=typer.prompt("Database password", default="pgvector"),
    )

    ingestion_config = LLMConfiguration(
        collection=typer.prompt("Unique collection name", default=path.name)
    )

    return ProjectConfiguration(
        name=project_name,
        include_project=include_project,
        project_src=project_src,
        llm=ingestion_config,
        db=db_config,
        sources=DUMMY_SOURCES,
    )


@init_cli.command("init", help="Initialize a new grimoire project")
def init(
    path: Path = typer.Argument(  # noqa: B008
        Path.cwd(),  # noqa: B008
        help="Path where grimoire project should be created",
    ),
) -> None:
    """
    Initialize a new grimoire project with questionaire.

    :param path: Path where grimoire project should be created.
    """
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

    success_message = f"""
    {green_text("Grimoire project initialized successfully! 🎉")}

    Configuration: {file_path}
    Note: directly modify the "{CONFIG_FILE_NAME}" configuration to your needs.
    """.strip()

    typer.echo(f"\n{success_message}\n")  # required for better formatting
