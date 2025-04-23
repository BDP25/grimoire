import yaml
from typer.testing import CliRunner

from grimoire.configuration import CONFIG_FILE_NAME
from grimoire.main import cli

runner = CliRunner()


def test_verify_command_no_config_file(tmp_path):
    result = runner.invoke(cli, ["verify", str(tmp_path)])
    assert result.exit_code == 1
    assert "No configuration file found" in result.output


def test_verify_command_with_valid_config(tmp_path):
    config_data = {
        "name": "test_project",
        "db": {
            "host": "localhost",
            "port": 5432,
            "db": "postgres",
            "user": "pgvector",
            "password": "pgvector",
        },
        "llm": {
            "collection": "test_collection",
            "k_results": 5,
            "score_threshold": 0.8,
            "lambda_mult": 0.5,
            "text_chunk_size": 512,
            "text_chunk_overlap": 128,
            "code_chunk_size": 512,
            "code_chunk_overlap": 128,
        },
        "include_project": True,
        "project_src": "test_project",
        "sources": [
            {
                "url": "https://github.com/pallets/flask",
                "include_md": True,
                "include_code": False,
            }
        ],
    }

    config_path = tmp_path / CONFIG_FILE_NAME
    with config_path.open("w") as f:
        yaml.dump(config_data, f)

    result = runner.invoke(cli, ["verify", str(tmp_path)])

    assert result.exit_code == 0
    assert "Verifying configuration" in result.output
    assert "Successful for: test_project" in result.output
