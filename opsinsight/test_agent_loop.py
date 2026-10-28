from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage

from opsinsight.agent_tools import AVAILABLE_TOOLS


MODEL_NAME = "qwen3:4b-instruct"


def main() -> None:
    model = ChatOllama(
        model=MODEL_NAME,
        temperature=0,
    )

    model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

    tools_by_name = {
        tool.name: tool for tool in AVAILABLE_TOOLS
    }

    messages = [
        HumanMessage(
            content=(
                "Produk apa saja yang memiliki stok pada atau "
                "di bawah batas minimum? Jelaskan berdasarkan "
                "data aktual. Jangan menebak."
            )
        )
    ]

    # Step 1: Ask the LLM whether a tool is needed.
    response = model_with_tools.invoke(messages)
    messages.append(response)

    # Step 2: Execute the tools requested by the LLM.
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name not in tools_by_name:
            raise ValueError(f"Unknown tool: {tool_name}")

        print(f"Executing tool: {tool_name}")

        result = tools_by_name[tool_name].invoke(tool_args)

        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

    # Step 3: Give the tool results back to the LLM.
    final_response = model_with_tools.invoke(messages)

    print("\n=== FINAL ANSWER ===")
    print(final_response.content)


if __name__ == "__main__":
    main()