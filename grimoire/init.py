from pathlib import Path

import typer

from grimoire.configuration import DBConfiguration, ProjectConfiguration

init_cli = typer.Typer()


@init_cli.command("init", help="Initialize a new grimoire project")
def init(
    path: Path = typer.Argument(  # noqa: B008
        Path.cwd(),  # noqa: B008
        help="Path where grimoire project should be created",
    ),
) -> None:
    if not path.exists():
        typer.echo(f"Error: Path {path} does not exist", err=True)
        raise typer.Exit(code=1)
    if path / "grimoire.yaml":
        overwrite = typer.confirm(
            f"File {path / 'grimoire.yaml'} already exists. Overwrite?"
        )
        if not overwrite:
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
    ).save_to_yaml(path)
    typer.echo(f"Configuration saved at {path / 'grimoire.yaml'}")
