from langgraph.graph import StateGraph, START, END

from state import AssistantState
from generator import Generator


def build_graph(generator: Generator):
   
    builder = StateGraph(AssistantState)
    builder.add_node("generate",
        lambda state: {
            "messages": [
                generator.generate(
                    state["messages"]
                )
            ]
        })

    builder.add_edge(
        START,
        "generate"
    )

    builder.add_edge(
        "generate",
        END
    )

    return builder.compile()