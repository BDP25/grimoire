import os

import torch
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

from grimoire.configuration import DBConfiguration


def embeddings() -> HuggingFaceEmbeddings:
    """
    Set up the embeddings for the application.

    :return: An instance of the HuggingFaceEmbeddings initialized with the specified model.
    """
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )

    # https://huggingface.co/BAAI/bge-m3?library=sentence-transformers
    # https://python.langchain.com/api_reference/huggingface/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True},
    )


def vectorstore_connection(db: DBConfiguration) -> str:
    """
    Set up the connection string for the vector store.

    :param db: Database configuration object containing connection details.
    :return: A connection string for the vector store.
    """
    return PGVector.connection_string_from_db_params(
        driver="psycopg",
        host=db.host,
        port=db.port,
        database=db.db,
        user=db.user,
        password=db.password,
    )


def setup_vectorstore(collection: str, connection: str) -> VectorStore | None:
    """
    Set up the vector store for the application.

    :param collection: Name of the collection to be used.
    :param connection: Connection string for the vector store.
    :return: An instance of the PGVector vector store initialized with the specified collection and connection.
    """
    try:
        return PGVector(
            collection_name=collection,
            connection=connection,
            embeddings=embeddings(),
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")
        return None


def clear_collection(collection: str, connection: str) -> None:
    """
    Clear the specified collection in the vector store.

    :param collection: Name of the collection to be cleared.
    :param connection: Connection string for the vector store.
    """
    try:
        PGVector(
            connection=connection,
            embeddings=embeddings(),
            collection_name=collection,
        ).delete_collection()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")


def delete_vectorstore(connection: str) -> None:
    """
    Delete the vector store.

    :param connection: Connection string for the vector store.
    """
    try:
        PGVector(
            connection=connection,
            embeddings=embeddings(),
        ).drop_tables()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")
