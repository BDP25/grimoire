from pathlib import Path
from typing import cast

from helpers import clear_vectorstore, setup_vectorstore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_text_splitters.markdown import Language, RecursiveCharacterTextSplitter


def ingest_code() -> None:
    clear_vectorstore()

    # Load code files using DirectoryLoader
    loader = DirectoryLoader(
        path="files", glob=["*.py", "*.js", "*.cpp", "*.java"], loader_cls=TextLoader
    )
    data = loader.load()

    splits = []
    for document in data:
        language = document.metadata.get("language")
        source = Path(document.metadata.get("source", ""))

        if language is None:
            try:
                language = Language(source.suffix[1:])
            except ValueError:
                language = None

        chunk_size, chunk_overlap = (512, 128)  # Default chunking settings

        if language:
            text_splitter = RecursiveCharacterTextSplitter.from_language(
                language=language,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

        chunks = text_splitter.split_text(document.page_content)
        splits.extend(
            [chunk for chunk in chunks if chunk.strip()]
        )  # Remove empty chunks

    documents = [
        Document(page_content=chunk, metadata=document.metadata) for chunk in splits
    ]

    vectorstore = setup_vectorstore("sandbox_code")
    vectorstore = cast(PGVector, vectorstore)
    vectorstore.add_documents(documents)


if __name__ == "__main__":
    ingest_code()
