from typer.testing import CliRunner

from grimoire.init import init_cli

runner = CliRunner()


def test_init_creates_configuration(tmp_path) -> None:
    result = runner.invoke(
        init_cli,
        [str(tmp_path)],
        input="\n".join(
            ["test-project", "localhost", "5432", "pgvector", "pgvector", "n"]
        ),
    )
    assert result.exit_code == 0
    assert (tmp_path / "grimoire.yaml").is_file()
    assert f"Configuration saved at {tmp_path / 'grimoire.yaml'}" in result.stdout


def test_init_uses_default_values(tmp_path) -> None:
    result = runner.invoke(init_cli, [str(tmp_path)], input="\n" * 5)

    config_content = (tmp_path / "grimoire.yaml").read_text()
    assert result.exit_code == 0
    assert f"name: {tmp_path.name}" in config_content
    assert "host: localhost" in config_content
    assert "port: 5432" in config_content
    assert "user: pgvector" in config_content
    assert "password: pgvector" in config_content


def test_init_uses_custom_chunk_values(tmp_path) -> None:
    result = runner.invoke(
        init_cli,
        [str(tmp_path)],
        input="\n".join(
            [
                "test-project",
                "localhost",
                "5432",
                "pgvector",
                "pgvector",
                "y",
                "256",
                "64",
                "512",
                "128",
            ]
        ),
    )

    config_content = (tmp_path / "grimoire.yaml").read_text()
    assert result.exit_code == 0
    assert "text_chunk_size: 256" in config_content
    assert "text_chunk_overlap: 64" in config_content
    assert "code_chunk_size: 512" in config_content
    assert "code_chunk_overlap: 128" in config_content


def test_init_fails_on_nonexistent_path() -> None:
    result = runner.invoke(init_cli, ["./nonexistent"])
    assert result.exit_code == 1
    assert "Error: Path nonexistent does not exist" in result.stdout


def test_init_overwrite_existing_file(tmp_path) -> None:
    config = tmp_path / "grimoire.yaml"
    config.touch()

    result = runner.invoke(
        init_cli,
        [str(tmp_path)],
        input="\n".join(
            ["y", "test-project", "localhost", "5432", "pgvector", "pgvector", "n"]
        ),
    )
    assert result.exit_code == 0
    assert (tmp_path / "grimoire.yaml").is_file()
    assert f"Configuration saved at {tmp_path / 'grimoire.yaml'}" in result.stdout


def test_init_does_not_overwrite_when_declined(tmp_path) -> None:
    config = tmp_path / "grimoire.yaml"
    config.touch()
    config.write_text("existing content")

    result = runner.invoke(init_cli, [str(tmp_path)], input="N\n")
    assert result.exit_code == 0
    assert "Exiting without overwriting existing file" in result.stdout
    assert config.read_text() == "existing content"
