from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json

from langgraph.errors import GraphRecursionError

from LangGraph.node_graph import build_graph

from models.models import UserQuery

# =========================
# FastAPI
# =========================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ FastAPI app initialized")

# ==========================
# INITIATING LLM
# ==========================

@app.get("/health")
def health():
    print("✅ /health called")
    return {"ok": True}


@app.post("/getrecommendations")
async def get_recommendations(user_input: UserQuery):
    """
    Generate travel and style recommendations using a LangGraph-based LLM workflow.

    This endpoint receives a structured user query and executes a multi-step
    LangGraph pipeline that streams intermediate results from different
    reasoning and recommendation nodes.

    The graph is executed in streaming mode, allowing the API to:
    - Collect intermediate reasoning steps
    - Aggregate outputs from multiple agents (e.g. travel and style recommenders)
    - Safely extract and compose a final response

    Workflow overview:
    1. Receives a `UserQuery` payload containing contextual data
       (e.g. user_id, event_id, preferences).
    2. Initializes the LangGraph execution with an empty recommendation state.
    3. Streams graph steps and stores intermediate node outputs.
    4. Extracts:
       - Travel recommendation text from the `travel_recommender` node
       - Image/style recommendations from the `style_recommender` node
    5. Returns a consolidated response aligned to the requesting user and event.

    Args:
        - user_input (UserQuery)
    Returns:
        - dict:

    Error Handling:
        - GraphRecursionError:
            Returned when the LangGraph execution exceeds its recursion limit,
            preventing infinite or cyclic graph execution.

        - Generic Exception:
            Catches any unexpected runtime error and returns the error message
            for debugging and observability purposes.

    Response Codes:
        200 OK:
            Recommendations were generated successfully.

        500 Internal Server Error:
            An unexpected error occurred during graph execution or response
            assembly.
    """
    print("\n🚀 API /getrecommendations called")
    print("Request body:", user_input.query)

    try:
        responses = []

        for step in build_graph().stream({"query": user_input.query, "recc": []}):
            print("\n🧩 Graph step:")
            print(step)
            responses.append(step)

        travel_recc = ""
        images = []

        for step in responses:
            if "travel_recommender" in step:
                travel_recc = step["travel_recommender"]["recc"][0]["travel_recc"]
            if "style_recommender" in step:
                images = step["style_recommender"]["recc"][0]["images"]

        final = {
            "travel_recc": travel_recc,
            "images": images,
            "user_id": user_input.query["user_id"],
            "event_id": user_input.query["event_id"],
        }

        print("\n✅ FINAL RESPONSE")
        print(json.dumps(final, indent=2, ensure_ascii=False))
        return {"response": final}

    except GraphRecursionError:
        print("❌ GraphRecursionError")
        return {"error": "Graph recursion limit reached"}

    except Exception as e:
        print("❌ UNHANDLED ERROR")
        print(e)
        return {"error": str(e)}
