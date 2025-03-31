from pathlib import Path
from typing import cast

from helpers import clear_collection, setup_vectorstore
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language import LanguageParser
from langchain_postgres import PGVector
from langchain_text_splitters.markdown import Language, RecursiveCharacterTextSplitter


def ingest_code(repo_path: Path) -> None:
    clear_collection("sandbox_code")
    data = GenericLoader.from_filesystem(
        path=repo_path,
        suffixes=[".py", ".js", ".ts", ".html", ".css"],
        parser=LanguageParser(),
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
                chunk_size=512,
                chunk_overlap=128,
            )
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=512, chunk_overlap=128
            )
        splits.extend(text_splitter.split_documents([document]))

    vectorstore = setup_vectorstore("sandbox_code")
    vectorstore = cast(PGVector, vectorstore)  # hack to avoid mypy error
    vectorstore.add_documents(splits)


if __name__ == "__main__":
    ingest_code(Path("files"))
