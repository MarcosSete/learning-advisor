from collections.abc import Sequence

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool


def execute_tool_calls(
    message: AIMessage,
    tools: Sequence[BaseTool],
) -> list[ToolMessage]:
    """Execute the tool calls requested in one AI message.

    This function executes only explicitly registered tools. It does not call the
    model again or implement an agent loop; orchestration remains a separate concern.
    """
    tools_by_name = {tool.name: tool for tool in tools}
    responses: list[ToolMessage] = []

    for tool_call in message.tool_calls:
        tool_name = tool_call["name"]
        tool = tools_by_name.get(tool_name)
        if tool is None:
            raise ValueError(f"Model requested an unregistered tool: {tool_name}")

        result = tool.invoke(tool_call["args"])
        responses.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

    return responses
