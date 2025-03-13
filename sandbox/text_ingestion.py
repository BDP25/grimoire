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


def ingest_text() -> None:
    clear_vectorstore()
    data = DirectoryLoader(path="files", glob="*.md", loader_cls=TextLoader).load()

    splits = []
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Heading1"),
            ("##", "Heading2"),
            ("###", "Heading3"),
        ],
        strip_headers=True,
    )

    for document in data:
        for split in md_splitter.split_text(document.page_content):
            splits.append(split)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
    chunks = text_splitter.split_documents(splits)

    vectorstore = setup_vectorstore("sandbox_text")
    vectorstore = cast(PGVector, vectorstore)  # hack to avoid mypy error
    vectorstore.add_documents(chunks)


if __name__ == "__main__":
    ingest_text()
