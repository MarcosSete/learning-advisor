from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from langchain_core.tools import BaseTool


class BaseToolCallingLLM(ABC):
    """Model capability for binding LangChain tools to a chat model."""

    @abstractmethod
    def bind_tools(self, tools: Sequence[BaseTool]) -> Any:
        """Return a model runnable with the supplied tools bound."""
        raise NotImplementedError
