from pathlib import Path
from typing import cast

from datasets import Dataset
from helpers import clear_vectorstore, setup_vectorstore
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


def load_files(directory: Path, encoding: str = "utf-8") -> Dataset:
    """Load all markdown files from the specified directory using Hugging Face Datasets."""
    file_paths = list(directory.glob("*.md"))
    texts = []

    # Iterate over the files and read their content
    for file_path in file_paths:
        try:
            with open(file_path, encoding=encoding) as file:
                # Append the text and metadata (file path) to the list
                texts.append(
                    {"text": file.read(), "metadata": {"source": str(file_path)}}
                )
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    # Create and return a Hugging Face Dataset from the list of text data
    return Dataset.from_list(texts)


def ingest_text() -> None:
    clear_vectorstore()

    # Define the directory where markdown files are stored
    data_directory = Path("files")
    if not data_directory.exists():
        raise FileNotFoundError(f"Directory not found: {data_directory}")

    # Load the files using Hugging Face Datasets
    dataset = load_files(data_directory, encoding="utf-8")

    splits = []
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS,
        strip_headers=True,
    )

    for document in dataset:
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
