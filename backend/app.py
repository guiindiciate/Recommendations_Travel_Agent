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
