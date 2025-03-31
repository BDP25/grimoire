import os
from pathlib import Path
from typing import Any

import torch
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language import LanguageParser
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters.markdown import (
    Language,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from grimoire.configuration import DBConfiguration, LLMConfiguration

HEADERS = [
    ("#", "Heading 1"),
    ("##", "Heading 2"),
    ("###", "Heading 3"),
    ("####", "Heading 4"),
    ("#####", "Heading 5"),
]


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
    path: Path, llm_config: LLMConfiguration, **kwargs: Any
) -> list[Document]:
    data = DirectoryLoader(
        path=str(path),
        glob=["**/*.md", "**/*.rst", "**/*.txt"],
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "UTF-8"},
        **kwargs,
    ).load()

    splits = []
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS,
        strip_headers=True,
    )

    for document in data:
        for split in md_splitter.split_text(document.page_content):
            splits.append(split)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=llm_config.text_chunk_size,
        chunk_overlap=llm_config.text_chunk_overlap,
    )
    return text_splitter.split_documents(splits)


def code_ingestion(
    path: Path, llm_config: LLMConfiguration, **kwargs: Any
) -> list[Document]:
    data = GenericLoader.from_filesystem(
        path=path,
        suffixes=[".py", ".js", ".ts", ".html", ".css"],
        parser=LanguageParser(),
        **kwargs,
    ).load()

    splits = []
    for document in data:
        language = document.metadata.get("language")
        source = Path(document.metadata.get("source", ""))
        if language is None:
            try:
                language = Language(source.suffix[1:])
            except ValueError:
                language = None

        if language:
            text_splitter = RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=llm_config.code_chunk_size,
                chunk_overlap=llm_config.code_chunk_overlap,
            )
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=llm_config.code_chunk_size,
                chunk_overlap=llm_config.code_chunk_overlap,
            )
        splits.extend(text_splitter.split_documents([document]))
    return splits
