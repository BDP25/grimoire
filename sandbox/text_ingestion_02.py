from typing import cast

from helpers import clear_vectorstore, setup_vectorstore
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    UnstructuredFileLoader,
)
from langchain_postgres import PGVector
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

TEXT_CHUNK_SIZE = 512
TEXT_CHUNK_OVERLAP = 128  # 20 - 30% of chunk size

HEADERS = [
    ("#", "Heading 1"),
    ("##", "Heading 2"),
    ("###", "Heading 3"),
    ("####", "Heading 4"),
    ("#####", "Heading 5"),
]


def load_documents() -> list:
    file_types = ["*.txt", "*.md", "*.pdf", "*.docx"]
    data = []

    for file_type in file_types:
        if file_type in {"*.pdf", "*.docx"}:
            loader_cls = UnstructuredFileLoader  # type: ignore
        else:
            loader_cls = TextLoader  # type: ignore

        loader = DirectoryLoader(path="files", glob=file_type, loader_cls=loader_cls)
        data.extend(loader.load())

    return data


def ingest_text() -> None:
    clear_vectorstore()
    data = load_documents()

    # Markdown-Splitter
    splits = []
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS, strip_headers=True
    )
    for document in data:
        splits.extend(md_splitter.split_text(document.page_content))

    # Recursive Character Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=128,
        separators=["\n\n", "\n", " "],
        length_function=len,
    )
    all_splits = text_splitter.split_documents(splits)

    # Ingest text into DB
    vectorstore = setup_vectorstore("sandbox_text")
    vectorstore = cast(PGVector, vectorstore)
    vectorstore.add_documents(all_splits)


if __name__ == "__main__":
    ingest_text()
