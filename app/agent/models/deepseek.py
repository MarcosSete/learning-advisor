from langchain_deepseek import ChatDeepSeek

from app.agent.models.base import BaseLLM
from app.infrastructure.config.settings import get_settings


class DeepSeekLLM(BaseLLM):
    """DeepSeek implementation of the BaseLLM interface."""

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY is not configured.")

        self._model = ChatDeepSeek(
            model=settings.deepseek_model,
            api_key=settings.deepseek_api_key,
            temperature=0,
        )

    def invoke(self, prompt: str) -> str:
        response = self._model.invoke(prompt)
        return response.content
