from langchain_deepseek import ChatDeepSeek

from app.agent.models.base import BaseLLM
from app.infrastructure.config.settings import get_settings

class DeepSeek(BaseLLM):
    """ DeepSeek implementation og the BaseLLM interface"""

    def __init__(self,) -> None:
        settings = get_settings()

        if not settings.deepseek_api_key:
            raise ValueError(
                "DEELSEEK_API_KEY IS NOT CONFIGURED"
            )

        self._model = ChatDeepSeek(
            model=settings.deepseek_model,
            api_key=settings.deepseek_api_key,
            temperature = 0
        )

    def invoke(self, prompt:str)-> str:
        response = self._model.invoke(prompt)
        return response.content