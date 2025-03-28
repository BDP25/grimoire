import os

import torch
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

from grimoire.configuration import DBConfiguration


def vectorstore_connection(db: DBConfiguration) -> str:
    return PGVector.connection_string_from_db_params(
        driver="psycopg",
        host=db.host,
        port=db.port,
        database="postgres",  # TODO: make this configurable
        user=db.user,
        password=db.password,
    )


def embeddings() -> HuggingFaceEmbeddings:
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


def setup_vectorstore(collection: str, connection: str) -> VectorStore | None:
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
    try:
        PGVector(
            connection=connection,
            embeddings=embeddings(),
            collection_name=collection,
        ).delete_collection()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")


def delete_vectorstore(connection: str) -> None:
    try:
        PGVector(
            connection=connection,
            embeddings=embeddings(),
        ).drop_tables()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")


def setup_llm() -> BaseChatModel:
    return init_chat_model(
        "google_genai:gemini-2.0-flash",
        api_key=os.getenv("LLM_API_KEY"),
        configurable_fields=None,
        max_tokens=512,
        temperature=0,
    )


def text_ingestion(
    collection: str, text_chunk_size: int, text_chunk_overlap: int
) -> None:
    pass


def code_ingestion(
    collection: str, code_chunk_size: int, code_chunk_overlap: int
) -> None:
    pass
