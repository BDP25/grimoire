import os

import torch
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector


def vectorstore_connection() -> str:
    return PGVector.connection_string_from_db_params(
        driver="psycopg",
        host="localhost",
        port=5432,
        database="postgres",
        user="pgvector",
        password="pgvector",
    )


def embeddings() -> HuggingFaceEmbeddings:
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.mps.is_available()
        else "cpu"
    )
    # https://huggingface.co/BAAI/bge-m3?library=sentence-transformers
    # https://python.langchain.com/api_reference/huggingface/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True},
    )


def setup_vectorstore(collection: str) -> VectorStore | None:
    try:
        return PGVector(
            collection_name=collection,
            connection=vectorstore_connection(),
            embeddings=embeddings(),
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")
        return None


def clear_vectorstore() -> None:
    try:
        PGVector(
            connection=vectorstore_connection(),
            embeddings=embeddings(),
        ).drop_tables()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")


def clear_collection(collection: str) -> None:
    try:
        PGVector(
            connection=vectorstore_connection(),
            embeddings=embeddings(),
            collection_name=collection,
        ).delete_collection()
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: {e}")


def setup_llm() -> BaseChatModel:
    return init_chat_model(
        model_provider="google_genai",
        model="gemini-2.0-flash",
        api_key=os.getenv("LLM_API_KEY"),
        temperature=0,
    )
