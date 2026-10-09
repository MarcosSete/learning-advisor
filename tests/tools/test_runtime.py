import pytest
from langchain_core.messages import AIMessage, ToolMessage

from app.agent.models.tool_calling import BaseToolCallingLLM
from app.tools.runtime import execute_tool_calls
from app.tools.text_tools import normalize_learning_topic


class FakeToolCallingLLM(BaseToolCallingLLM):
    def __init__(self):
        self.bound_tools = None

    def bind_tools(self, tools):
        self.bound_tools = list(tools)
        return self


def test_model_capability_can_bind_the_local_topic_tool():
    model = FakeToolCallingLLM()

    bound_model = model.bind_tools([normalize_learning_topic])

    assert bound_model is model
    assert [tool.name for tool in model.bound_tools] == [
        "normalize_learning_topic"
    ]


def test_execute_tool_calls_runs_registered_tool_and_returns_tool_message():
    message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "normalize_learning_topic",
                "args": {"topic": "  graph   machine learning "},
                "id": "call_123",
                "type": "tool_call",
            }
        ],
    )

    responses = execute_tool_calls(message, [normalize_learning_topic])

    assert len(responses) == 1
    assert isinstance(responses[0], ToolMessage)
    assert responses[0].content == "graph machine learning"
    assert responses[0].tool_call_id == "call_123"


def test_execute_tool_calls_rejects_unregistered_tool():
    message = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "delete_catalog",
                "args": {},
                "id": "call_456",
                "type": "tool_call",
            }
        ],
    )

    with pytest.raises(ValueError, match="unregistered tool: delete_catalog"):
        execute_tool_calls(message, [normalize_learning_topic])
