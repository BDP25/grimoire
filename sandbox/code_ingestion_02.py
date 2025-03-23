from pathlib import Path
from typing import cast

from helpers import clear_vectorstore, setup_vectorstore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_postgres import PGVector
from tree_sitter import Node
from tree_sitter_languages import get_parser

GLOB_PATTERNS = ["*.py", "*.js", "*.cpp", "*.java"]
CHUNK_SIZE = 512
CHUNK_OVERLAP = 128


def extract_code_chunks(code: str, ext: str) -> list[str]:
    try:
        parser = get_parser(ext)
    except Exception:
        return [code]  # Fallback to raw code if no parser found

    tree = parser.parse(code.encode())
    root = tree.root_node

    chunks = []
    visited = set()

    def visit(node: Node) -> None:
        if node.id in visited:
            return
        visited.add(node.id)

        if node.type in [
            "function_definition",
            "method_definition",
            "class_declaration",
        ]:
            snippet = code[node.start_byte : node.end_byte].strip()
            if snippet:
                chunks.append(snippet)

        for child in node.children:
            visit(child)

    visit(root)
    return chunks or [code]


def ingest_code() -> None:
    clear_vectorstore()

    loader = DirectoryLoader(
        path="files",
        glob=GLOB_PATTERNS,
        loader_cls=TextLoader,
    )
    data = loader.load()

    documents = []
    for doc in data:
        source = Path(doc.metadata.get("source", ""))
        ext = source.suffix[1:]
        chunks = extract_code_chunks(doc.page_content, ext)

        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata=doc.metadata))

    vectorstore = setup_vectorstore("sandbox_code")
    vectorstore = cast(PGVector, vectorstore)
    vectorstore.add_documents(documents)


if __name__ == "__main__":
    ingest_code()
