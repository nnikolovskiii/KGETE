import os
from enum import Enum

from dotenv import load_dotenv

from app.llms.nim_chat import chat_with_nim
from app.llms.ollama_chat import chat_with_ollama
from app.llms.openai_chat import chat_with_openai


class ChatModel(Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"
    NIM = "nim"


def generic_chat(
        message: str
) -> str:
    load_dotenv()

    chat_model = os.getenv("CHAT_MODEL")

    if chat_model == ChatModel.OPENAI.value:
        return chat_with_openai(message)
    elif chat_model == ChatModel.OLLAMA.value:
        return chat_with_ollama(message)
    elif chat_model == ChatModel.NIM.value:
        return chat_with_nim(message)
