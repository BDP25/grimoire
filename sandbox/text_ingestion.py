from typing import cast

from helpers import clear_vectorstore, setup_vectorstore
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_postgres import PGVector
from langchain_text_splitters.markdown import (
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


def ingest_text() -> None:
    clear_vectorstore()
    data = DirectoryLoader(
        path="files",
        glob="*.md",
        loader_cls=TextLoader,
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
        chunk_size=TEXT_CHUNK_SIZE, chunk_overlap=TEXT_CHUNK_OVERLAP
    )
    all_splits = text_splitter.split_documents(splits)

    vectorstore = setup_vectorstore("sandbox_text")
    vectorstore = cast(PGVector, vectorstore)  # hack to avoid mypy error
    vectorstore.add_documents(all_splits)


if __name__ == "__main__":
    ingest_text()
