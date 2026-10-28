import logging

from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from opsinsight.agent_tools import AVAILABLE_TOOLS

logger = logging.getLogger(__name__)

MODEL_NAME = "qwen3:4b-instruct"


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


model = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
    num_predict=512,
)

model_with_tools = model.bind_tools(AVAILABLE_TOOLS)


def call_model(state: AgentState) -> dict:
    """Ask the LLM to respond or request a tool."""
    system_instruction = {
        "role": "system",
        "content": (
            "You are OpsInsight, an AI sales and inventory analyst. "
            "Always respond in the same language as the user's question. "
            "You have access to tools that retrieve actual business data. "
            "When a question requires business facts, call the relevant tools "
            "before answering. Do not ask the user for permission to call tools. "
            "Use tool results as the source of truth. "
            "Never invent figures, products, or dates. "
            "Do not judge sales performance as good or bad without a target "
            "or comparison data. If the data is insufficient, explain why."
        ),
    }

    messages = [system_instruction, *state["messages"]]
    response = model_with_tools.invoke(messages)

    logger.debug("Agent node executed.")
    logger.debug("Tool calls: %s", response.tool_calls)

    return {"messages": [response]}    

builder = StateGraph(AgentState)

# Register the workflow nodes.
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(AVAILABLE_TOOLS))

# Define the workflow edges.
builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition,
)

builder.add_edge("tools", "agent")

# Compile the graph into an executable application
graph = builder.compile()


def ask_agent(question: str) -> str:
    """Run the agent workflow and return its final answer."""
    if not question.strip():
        raise ValueError("Question must not be empty.")
    
    result = graph.invoke(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        config={
            "recursion_limit": 10,
        }
    )

    final_message = result["messages"][-1]

    if not isinstance(final_message.content, str):
        raise RuntimeError("Agent returned an unexpected response.")

    if not final_message.content.strip():
        raise RuntimeError("Agent returned an empty answer.")

    return final_message.content


if __name__ == "__main__":
    question = (
        "Buat ringkasan kondisi bisnis berdasarkan data yang tersedia. "
        "Sebutkan total pendapatan, jumlah unit terjual, "
        "tiga produk terlaris berdasarkan unit, dan produk "
        "yang stoknya pada atau di bawah batas minimum. "
        "Gunakan data dari database dan jangan mengarang angka."
    )

    answer = ask_agent(question)

    print("=== OPSINSIGHT AI AGENT ===")
    print(answer)