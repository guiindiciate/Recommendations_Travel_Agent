# =========================
# LangGraph
# =========================

from langgraph.graph import StateGraph, START, END
from LangGraph.models.models import AgentState
from ChatGPT_Model.tools import travel_recommender_tool, style_recommender_tool
import json

def travel_node(state: AgentState):
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
