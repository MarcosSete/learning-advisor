from collections.abc import Sequence

from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool

from app.tools.runtime import execute_tool_calls


def invoke_with_tools(
    model_with_tools: Runnable,
    messages: Sequence[BaseMessage],
    tools: Sequence[BaseTool],
) -> AIMessage:
    """Run one tool-call round and ask the model for its final response.

    Multiple tool calls in the first AI message are supported. Repeated tool-call
    rounds are intentionally left to the orchestration layer.
    """
    conversation = list(messages)
    ai_message = model_with_tools.invoke(conversation)

    if not isinstance(ai_message, AIMessage):
        raise TypeError("Tool-capable chat model must return an AIMessage")

    if not ai_message.tool_calls:
        return ai_message

    conversation.append(ai_message)
    conversation.extend(execute_tool_calls(ai_message, tools))

    final_message = model_with_tools.invoke(conversation)
    if not isinstance(final_message, AIMessage):
        raise TypeError("Tool-capable chat model must return an AIMessage")
    if final_message.tool_calls:
        raise RuntimeError(
            "Model requested another tool round; multi-round orchestration "
            "is not implemented yet"
        )

    return final_message
