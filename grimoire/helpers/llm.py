import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel


def setup_llm() -> BaseChatModel:
    """
    Set up the LLM (Language Model) for the application.

    :return: An instance of the chat model initialized with the specified parameters.
    """
    return init_chat_model(
        "google_genai:gemini-2.0-flash",
        api_key=os.getenv("LLM_API_KEY"),
        configurable_fields=None,
        max_tokens=512,
        temperature=0,
    )
