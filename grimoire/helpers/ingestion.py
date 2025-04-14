from pathlib import Path
from typing import Any

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language import LanguageParser
from langchain_core.documents import Document
from langchain_text_splitters.markdown import (
    Language,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from grimoire.configuration import LLMConfiguration

HEADERS = [
    ("#", "Heading 1"),
    ("##", "Heading 2"),
    ("###", "Heading 3"),
    ("####", "Heading 4"),
    ("#####", "Heading 5"),
]


def text_ingestion(
    path: Path, llm_config: LLMConfiguration, **kwargs: Any
) -> list[Document]:
    """
    Ingests text files from a directory and splits them into smaller chunks.

    :param path: Path to the directory containing text files.
    :param llm_config: Configuration object containing chunk size and overlap settings.
    :param kwargs: Additional arguments for the DirectoryLoader.
    :return: List of Document objects representing the ingested and split text.
    """
    data = DirectoryLoader(
        path=str(path),
        glob=["*.md", "*.txt", "*.rsd", "*.rst"],
        recursive=True,
        use_multithreading=True,
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
    """
    Ingests code files from a directory and splits them into smaller chunks.

    :param path: Path to the directory containing code files.
    :param llm_config: Configuration object containing chunk size and overlap settings.
    :param kwargs: Additional arguments for the GenericLoader.
    :return: List of Document objects representing the ingested and split code.
    """
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
