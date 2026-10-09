import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.tools.conversation import invoke_with_tools
from app.tools.text_tools import normalize_learning_topic


class FakeRunnable:
    def __init__(self, responses):
        self.responses = list(responses)
        self.received_messages = []

    def invoke(self, messages):
        self.received_messages.append(list(messages))
        return self.responses.pop(0)


def test_invoke_with_tools_returns_final_response_after_tool_result():
    tool_request = AIMessage(
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
    final_response = AIMessage(content="Normalized topic: graph machine learning")
    model = FakeRunnable([tool_request, final_response])
    initial_messages = [HumanMessage(content="Normalize graph topic")]

    result = invoke_with_tools(
        model,
        initial_messages,
        [normalize_learning_topic],
    )

    assert result.content == "Normalized topic: graph machine learning"
    assert len(model.received_messages) == 2
    second_call_messages = model.received_messages[1]
    assert second_call_messages[-2].tool_call_id == "call_123"
    assert isinstance(second_call_messages[-1], ToolMessage)
    assert second_call_messages[-1].content == "graph machine learning"
    assert len(initial_messages) == 1


def test_invoke_with_tools_returns_direct_response_when_no_tool_is_needed():
    model = FakeRunnable([AIMessage(content="No tool needed")])

    result = invoke_with_tools(
        model,
        [HumanMessage(content="Say hello")],
        [normalize_learning_topic],
    )

    assert result.content == "No tool needed"
    assert len(model.received_messages) == 1


def test_invoke_with_tools_rejects_unbounded_second_tool_round():
    first_response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "normalize_learning_topic",
                "args": {"topic": "graphs"},
                "id": "call_123",
                "type": "tool_call",
            }
        ],
    )
    second_response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "normalize_learning_topic",
                "args": {"topic": "graphs"},
                "id": "call_456",
                "type": "tool_call",
            }
        ],
    )
    model = FakeRunnable([first_response, second_response])

    with pytest.raises(RuntimeError, match="multi-round orchestration"):
        invoke_with_tools(
            model,
            [HumanMessage(content="Normalize graphs")],
            [normalize_learning_topic],
        )
