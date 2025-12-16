from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv() 

llm = ChatOpenAI(model="gpt-4o", temperature=0)
print("🤖 ChatOpenAI initialized")

# =========================
# Travel LLM
# =========================
def call_travel_llm(user_details: dict) -> str:
    print("\n➡️ [LLM] call_travel_llm called")
    print("Payload:", user_details)

    try:
        system = (
            "You are an upbeat, no-fluff travel assistant. Deliver short, tactical suggestions that a "
            "traveler can act on immediately. Focus on the event city and date window; keep answers under "
            "120 words.\n"
            "- Cover: best areas to stay (1-2), 2-3 must-do sights/food, quick transit tips, and 1 weather/packing note.\n"
            "- Tailor to the event type (e.g., wedding, conference, festival) and the location season.\n"
            "- Infer season and typical weather from the date/location; adjust suggestions for the place type "
            "(urban, beach, mountain, countryside) when obvious.\n"
            "- If details are missing, make sensible defaults and continue; never ask the user for more info.\n"
            "- No lists longer than 4 items; no emojis; avoid generic filler."
        )
        user = f"""
Location: {user_details["event_location"]}
Event: {user_details["event_type"]}
Date: {user_details["event_date"]}
"""

        response = llm.invoke([
            SystemMessage(content=system),
            HumanMessage(content=user)
        ])

        print("⬅️ [LLM] response received")
        print(response.content)
        return response.content

    except Exception as e:
        print("❌ ERROR in call_travel_llm")
        print(e)
        raise
