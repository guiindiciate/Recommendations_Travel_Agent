# =========================
# LangGraph
# =========================

from langgraph.graph import StateGraph, START, END
from LangGraph.models.models import AgentState
from ChatGPT_Model.tools import travel_recommender_tool, style_recommender_tool
import json

def travel_node(state: AgentState):
    """
    LangGraph node responsible for generating travel recommendations.

    This node extracts event and user context from the graph state,
    invokes the `travel_recommender_tool`, and normalizes the output
    into the graph's expected recommendation format.

    Args:
        state (AgentState):
            Current LangGraph state containing the user query and
            accumulated recommendations.

    Returns:
        dict:
            A partial state update with travel recommendations, structured as:
            {
                "recc": [
                    {
                        "travel_recc": "<LLM-generated travel text>"
                    }
                ]
            }
    """
    print("\n🔗 [GRAPH] travel_node entered")
    q = state["query"]

    tool_args = {
        "gender": q["gender"],
        "event_date": q["event_date"],
        "event_location": q["event_location"],
        "event_type": q["event_name"],
    }
    print("➡️ travel_node tool_args:", tool_args)

    result = travel_recommender_tool.invoke(tool_args)

    print("⬅️ travel_node result:", result)
    return {"recc": [{"travel_recc": result}]}


def style_node(state: AgentState):
    """
    LangGraph node responsible for generating style and image recommendations.

    This node invokes the `style_recommender_tool` using event context
    extracted from the graph state. The tool response is expected to be
    a JSON-formatted string containing image results.

    The node safely parses the JSON output and falls back to empty
    values if parsing fails, ensuring graph stability.

    Args:
        state (AgentState):
            Current LangGraph state containing the user query and
            accumulated recommendations.

    Returns:
        dict:
            A partial state update with style recommendations, structured as:
            {
                "recc": [
                    {
                        "images": [<image_url>, ...],
                        "image_query": "<search query used to fetch images>"
                    }
                ]
            }
    """
    print("\n🔗 [GRAPH] style_node entered")
    q = state["query"]

    tool_args = {
        "gender": q["gender"],
        "event_date": q["event_date"],
        "event_location": q["event_location"],
        "event_type": q["event_name"],
    }
    print("➡️ style_node tool_args:", tool_args)

    result = style_recommender_tool.invoke(tool_args)

    print("⬅️ style_node raw result:", result)

    try:
        parsed = json.loads(result)
        images = parsed.get("results", [])
        image_query = parsed.get("query")
    except Exception as e:
        print("❌ JSON parse error in style_node:", e)
        images = []
        image_query = None

    return {"recc": [{"images": images, "image_query": image_query}]}



def build_graph():
    """
    Build and compile the LangGraph recommendation workflow.

    This graph executes travel and style recommendation nodes in parallel
    from the START state and terminates once both nodes complete execution.

    Graph structure:
        START
          ├── travel_recommender ──► END
          └── style_recommender  ──► END

    Returns:
        StateGraph:
            A compiled LangGraph instance ready for streaming or
            synchronous execution.
    """
    builder = StateGraph(AgentState)
    builder.add_node("travel_recommender", travel_node)
    builder.add_node("style_recommender", style_node)

    builder.add_edge(START, "travel_recommender")
    builder.add_edge(START, "style_recommender")
    builder.add_edge("travel_recommender", END)
    builder.add_edge("style_recommender", END)

    graph = builder.compile()
    print("🧠 LangGraph compiled")
    return graph
