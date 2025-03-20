from typing import cast

from helpers import clear_vectorstore, setup_vectorstore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

TEXT_CHUNK_SIZE = 512
TEXT_CHUNK_OVERLAP = 128  # 20 - 30% Overlap


def ingest_text() -> None:
    clear_vectorstore()

    data = DirectoryLoader(
        path="files",
        glob="*.md",
        loader_cls=TextLoader,
    ).load()

    # Split Text in Chunks
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TEXT_CHUNK_SIZE,
        chunk_overlap=TEXT_CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],  # Splits first by paragraphs, then lines
    )

    splits = []
    for document in data:
        splits.extend(char_splitter.split_text(document.page_content))

    documents = [Document(page_content=chunk) for chunk in splits]

    # Ingest into DB
    vectorstore = setup_vectorstore("sandbox_text")
    vectorstore = cast(PGVector, vectorstore)
    vectorstore.add_documents(documents)


if __name__ == "__main__":
    ingest_text()
