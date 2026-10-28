from langchain_ollama import ChatOllama

from opsinsight.agent_tools import AVAILABLE_TOOLS


MODEL_NAME = "qwen3:4b-instruct"


def main() -> None:
    model = ChatOllama(
        model=MODEL_NAME,
        temperature=0,
    )

    model_with_tools = model.bind_tools(AVAILABLE_TOOLS)

    question = (
        "Produk apa saja yang memiliki stok pada atau di bawah "
        "batas minimum? Gunakan tool yang paling relevan. "
        "Jangan menebak berdasarkan pengetahuan sendiri."
    )

    response = model_with_tools.invoke(question)

    print("=== MODEL RESPONSE ===")
    print(response.content)

    print("\n=== REQUESTED TOOL CALLS ===")

    if not response.tool_calls:
        print("Model did not request a tool call.")
        return

    for tool_call in response.tool_calls:
        print(f"Tool name: {tool_call['name']}")
        print(f"Arguments: {tool_call['args']}")


if __name__ == "__main__":
    main()