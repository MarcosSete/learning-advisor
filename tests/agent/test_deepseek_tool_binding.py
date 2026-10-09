from app.agent.models.deepseek import DeepSeekLLM
from app.tools.text_tools import normalize_learning_topic


class FakeChatModel:
    def __init__(self):
        self.bound_tools = None

    def bind_tools(self, tools):
        self.bound_tools = tools
        return "bound-model"


def test_deepseek_llm_delegates_tool_binding_without_api_call():
    llm = DeepSeekLLM.__new__(DeepSeekLLM)
    fake_model = FakeChatModel()
    llm._model = fake_model

    result = llm.bind_tools([normalize_learning_topic])

    assert result == "bound-model"
    assert fake_model.bound_tools == [normalize_learning_topic]
