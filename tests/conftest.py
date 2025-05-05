from collections.abc import Callable
from pathlib import Path

import pytest
from typer.testing import CliRunner

from grimoire.main import cli


@pytest.fixture()
def create_grimoire_config(tmp_path) -> Callable:
    def _create_grimoire_config() -> Path:
        runner = CliRunner()
        runner.invoke(
            cli,
            ["init", str(tmp_path)],
            input="\n".join(
                [
                    "test-project",
                    "y",
                    "grimoire",
                    "localhost",
                    "5432",
                    "postgres",
                    "pgvector",
                    "pgvector",
                    "mycollection",
                ]
            ),
        )
        return tmp_path

    return _create_grimoire_config


@pytest.fixture()
def config_data() -> dict:
    return {
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
