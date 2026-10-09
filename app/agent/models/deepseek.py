from collections.abc import Sequence
from typing import Any

from langchain_core.tools import BaseTool
from langchain_deepseek import ChatDeepSeek

from app.agent.models.base import BaseLLM
from app.agent.models.tool_calling import BaseToolCallingLLM
from app.infrastructure.config.settings import get_settings


class DeepSeekLLM(BaseLLM, BaseToolCallingLLM):
    """DeepSeek implementation for text generation and tool calling."""

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

    def bind_tools(self, tools: Sequence[BaseTool]) -> Any:
        """Return a DeepSeek chat model with the supplied tools registered."""
        return self._model.bind_tools(list(tools))
