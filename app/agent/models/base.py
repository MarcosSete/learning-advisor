from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Generate a response for the given prompt."""
        raise NotImplementedError