from pathlib import Path

import typer

from grimoire.configuration import (
    CONFIG_FILE_NAME,
    CodeSource,
    DBConfiguration,
    DocumentSource,
    ProjectConfiguration,
)

init_cli = typer.Typer()

DUMMY_DOCS = [
    DocumentSource(
        site_url="https://numpy.org/doc/stable/",
        url="https://github.com/numpy/numpy",
    ),
    DocumentSource(
        site_url="https://pandas.pydata.org/docs/",
        url="https://github.com/pandas-dev/pandas",
        exclude=[
            "doc/.gitignore",
            "doc/redirects.csv",
            "doc/scripts/*",
            "doc/cheatsheet/*",
        ],
        include=["doc"],
    ),
]

DUMMY_CODE = [
    CodeSource(
        url="https://github.com/pandas-dev/pandas",
        path="pandas",
    )
]


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

    project_name = typer.prompt("Project name", default=path.name)
    db_host = typer.prompt("Database host", default="localhost")
    db_port = typer.prompt("Database port", default="5432")
    db_user = typer.prompt("Database user", default="pgvector")
    db_password = typer.prompt("Database password", default="pgvector")

    ProjectConfiguration(
        name=project_name,
        db=DBConfiguration(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
        ),
        docs=DUMMY_DOCS,
        code=DUMMY_CODE,
    ).save_to_yaml(file_path)
    typer.echo(f"Configuration saved at {file_path}")
