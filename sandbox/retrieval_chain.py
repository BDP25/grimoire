import os
from typing import Any

from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableSerializable,
)
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from pydantic import SecretStr

# Load API key
load_dotenv()

PGVECTOR_CONNECTION_STRING = (
    "postgresql+psycopg2://pgvector:pgvector@localhost:5432/pgvector"
)
COLLECTION_NAME = "sandbox_text"
LLM_API_KEY = SecretStr(os.getenv("LLM_API_KEY"))  # type: ignore

# Initialize Google Gemini embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=LLM_API_KEY
)


# Connect to PGVector database
def connect_pgvector() -> PGVector:
    """Loads the existing PGVector vector store."""
    try:
        vectorstore = PGVector.from_existing_index(
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            connection=PGVECTOR_CONNECTION_STRING,
            use_jsonb=True,
        )
    except Exception as e:
        print(f"Error connecting to PGVector: {e}")
        raise

    return vectorstore


# System message for the AI assistant
SYSTEM_MESSAGE = """Your name is grimoire. You are a conversational AI assistant. """  # TODO: add rules

# Chat prompt template for the LLM
PROMPT_TEMPLATE = """
Context: {context}

History: {chat_history}

Question: {question}
Answer:
"""


# Function to retrieve and manage chat history
def get_chat_memory(messages: list[dict[str, Any]]) -> ConversationBufferMemory:
    """Retrieves chat history and stores previous conversations."""
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    for msg in messages:
        memory.save_context({"input": msg["question"]}, {"output": msg["answer"]})
    return memory


# Function to build the retrieval chain
def build_chain(messages: list[dict[str, Any]]) -> RunnableSerializable:
    """Creates a retrieval chain that retrieves documents and generates an AI response."""
    try:
        vectorstore = connect_pgvector()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    except Exception as e:
        print(f"Error connecting to PGVector: {e}")
        raise

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_MESSAGE),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(PROMPT_TEMPLATE),
        ]
    )
    ChatPromptTemplate.input_variables = ["chat_history", "context", "question"]
    memory = get_chat_memory(messages)

    # Document retrieval + LLM integration
    setup_and_retrieval = RunnableParallel(
        {  # type: ignore
            "context": retriever,
            "question": RunnablePassthrough(),
            "chat_history": memory.load_memory_variables,
        }
    )

    # Google Generative AI als LLM nutzen
    llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=LLM_API_KEY)

    # Chain mit LLM
    return setup_and_retrieval | prompt | llm | StrOutputParser()


if __name__ == "__main__":
    chain = build_chain([])
    result = chain.invoke({"question": "Who knows Volka?"})
    print("Answer:", result)
