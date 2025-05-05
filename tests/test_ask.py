import os
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from grimoire.main import cli

runner = CliRunner()


@patch.dict(os.environ, {}, clear=True)
def test_ask_fails_without_llm_api_key(create_grimoire_config):
    path = create_grimoire_config()
    result = runner.invoke(cli, ["ask", "What", "is", "this?", "--path", str(path)])
    assert result.exit_code != 0
    assert "LLM_API_KEY environment variable is not set." in result.stdout


@patch.dict(os.environ, {"LLM_API_KEY": "fake-key"})
@patch("grimoire.ask.setup_llm")
def test_ask_with_skip_rag_uses_only_llm(mock_setup_llm, create_grimoire_config):
    path = create_grimoire_config()
    mock_llm = MagicMock()
    mock_llm.stream.return_value = [MagicMock(content="LLM response.")]
    mock_setup_llm.return_value = mock_llm

    result = runner.invoke(
        cli, ["ask", "My dummy question?", "--skip-rag", "--path", str(path)]
    )
    assert result.exit_code == 0
    assert "LLM response." in result.stdout
    mock_llm.stream.assert_called_once_with("My dummy question?")


@patch.dict(os.environ, {"LLM_API_KEY": "fake-key"})
@patch("grimoire.ask.setup_llm")
@patch("grimoire.ask.ProjectConfiguration.load_from_yaml")
@patch("grimoire.ask.vectorstore_connection")
@patch("grimoire.ask.setup_vectorstore")
@patch("grimoire.ask.get_retrieval_chain")
def test_ask_with_rag_invokes_rag_chain(
    mock_get_chain,
    mock_setup_vectorstore,
    mock_vectorstore_connection,
    mock_load_config,
    mock_setup_llm,
    create_grimoire_config,
):
    path = create_grimoire_config()
    mock_llm = MagicMock()
    mock_setup_llm.return_value = mock_llm

    mock_config = MagicMock()
    mock_config.llm.collection = "test"
    mock_config.db = {}
    mock_load_config.return_value = mock_config

    mock_vectorstore = MagicMock()
    mock_setup_vectorstore.return_value = mock_vectorstore

    mock_chain = MagicMock()
    mock_chain.stream.return_value = ["retrieved result"]
    mock_get_chain.return_value = mock_chain

    result = runner.invoke(cli, ["ask", "Some", "question", "--path", str(path)])
    assert result.exit_code == 0
    assert "retrieved result" in result.stdout
    mock_load_config.assert_called_once()
    mock_vectorstore_connection.assert_called_once_with(mock_config.db)
    mock_setup_vectorstore.assert_called_once_with(
        mock_config.llm.collection, mock_vectorstore_connection.return_value
    )
    mock_get_chain.assert_called_once_with(
        mock_setup_vectorstore.return_value,
        mock_setup_llm.return_value,
        mock_config.llm,
    )
    mock_chain.stream.assert_called_once_with("Some question")
