import os
from collections.abc import Generator
from typing import cast

from helpers import setup_llm, setup_vectorstore
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_core.vectorstores import VectorStore

SYSTEM_MESSAGE = """

Your name is grimoire. You are an AI assistent who helps with questions about code and projects.

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

# suppress grpc and glog logs
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_MINLOGLEVEL"] = "2"


def build_retrieval_chain() -> RunnableSerializable:
    llm = setup_llm()

    vectorstore = setup_vectorstore("sandbox_text")
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
            "context": vectorstore.as_retriever(),
            "question": RunnablePassthrough(),
        }
    )

    return retrieval | prompt | llm | StrOutputParser()


def stream_response(chain: RunnableSerializable, question: str) -> Generator:
    for chunk in chain.stream(question):
        if chunk is not None:
            yield chunk


if __name__ == "__main__":
    chain = build_retrieval_chain()

    question = "What is Vilko?"
    for chunk in stream_response(chain, question):
        print(chunk)

    question = "What happened to Strubelpeter?"
    for chunk in stream_response(chain, question):
        print(chunk)

    question = "How to create multi-page documentation in Markdown?"
    for chunk in stream_response(chain, question):
        print(chunk)
