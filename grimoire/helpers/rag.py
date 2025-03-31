import os
from pathlib import Path
from typing import Any, cast

import torch
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language import LanguageParser
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableSerializable,
)
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

SYSTEM_MESSAGE = """

Your name is grimoire. You are an AI assistant who helps with questions about code and projects.

Rules:
- Do not make up an answer if you do not know the answer, just say that you do not know the answer.
- Ask for clarification if the question is vague.
- If the context is not relevant, then answer with your best knowledge about the topic.
- If you answer with your best knowledge, then say it that the answer is based on your general knowledge.
- Answer the question shortly and clearly and do not provide too much information.
- Provide accurate, efficient, and maintainable code solutions.
- Promote secure coding practices and avoid security vulnerabilities.
- Do not copy proprietary or copyrighted code.
- Give credit when using open-source examples.
- Ensure fair, unbiased, and professional responses.
- Encourage best practices and explain concepts when needed.
- Do not store, misuse, or expose sensitive user data.
"""

PROMPT_TEMPLATE = """
Context: {context}

Question: {question}

Answer:
"""


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


def get_retrieval_chain(collection: str, connection: str) -> RunnableSerializable:
    # suppress grpc and glog logs
    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GLOG_MINLOGLEVEL"] = "2"

    llm = setup_llm()

    vectorstore = setup_vectorstore(collection, connection)
    vectorstore = cast(VectorStore, vectorstore)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(PROMPT_TEMPLATE),
        ]
    )

    ChatPromptTemplate.input_variables = ["context", "question"]

    retrieval = RunnableParallel(
        {  # type: ignore
            # TODO: add generic search_kwargs from config
            "context": vectorstore.as_retriever(),
            "question": RunnablePassthrough(),
        }
    )

    return retrieval | prompt | llm | StrOutputParser()


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
