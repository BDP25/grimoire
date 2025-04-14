import os

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_core.vectorstores import VectorStore

from grimoire.configuration import LLMConfiguration

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


def get_retrieval_chain(
    vectorstore: VectorStore, llm: BaseChatModel, config: LLMConfiguration
) -> RunnableSerializable:
    """
    Creates a retrieval chain using the provided vectorstore and LLM.

    :param vectorstore: The vector store to use for retrieval.
    :param llm: The language model to use for generating responses.
    :param config: Configuration object containing LLM settings.
    :return: A RunnableSerializable object representing the retrieval chain.
    """
    # suppress grpc and glog logs
    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GLOG_MINLOGLEVEL"] = "2"

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(PROMPT_TEMPLATE),
        ]
    )

    ChatPromptTemplate.input_variables = ["context", "question"]

    retrieval = RunnableParallel(
        {  # type: ignore
            "context": vectorstore.as_retriever(
                search_kwargs={
                    "k": config.k_results,
                    "score_threshold": config.score_threshold,
                    "lambda_mult": config.lambda_mult,
                }
            ),
            "question": RunnablePassthrough(),
        }
    )

    return retrieval | prompt | llm | StrOutputParser()
