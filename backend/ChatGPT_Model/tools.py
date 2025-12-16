import os
import requests
import json


from ChatGPT_Model.llm import call_travel_llm

from langchain_core.tools import tool

from dotenv import load_dotenv

load_dotenv()



SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# =========================
# STYLE TOOL (IMAGES)
# =========================
@tool
def style_recommender_tool(
    gender: str,
    event_date: str,
    event_location: str,
    event_type: str,
) -> str:
    """Search Google Images (via SerpAPI) for outfit inspiration and return image links as JSON.

    Use this tool when the user wants visual outfit ideas or styling inspiration for a specific
    event. It builds a Google Images query from the provided inputs and fetches up to 10 image
    results through SerpAPI.

    Args:
        gender: Free-form description (e.g., "male", "female", "masculino"). Maps to "men"/"women" in query.
        event_date: Date or season text used to bias results toward relevant weather/seasonality.
        event_location: City/region/country; added to the query to localize the look.
        event_type: Occasion name (e.g., wedding, business meeting, music festival).

    Returns:
        JSON string with:
            - query: The exact Google Images query string used.
            - results: List of up to 10 items, each containing title, image_url, thumbnail, link, source.

    Notes:
        - Requires SERPAPI_API_KEY to be set in the environment.
        - Intended for inspiration only (no shopping links guaranteed).
        - Prefer this tool over text-only recommendations when the user asks for images or examples of looks.
    """
    print("\n🎨 [STYLE TOOL] called")
    print("Inputs:", gender, event_date, event_location, event_type)

    if not SERPAPI_API_KEY:
        print("❌ SERPAPI_API_KEY missing")
        raise RuntimeError("SERPAPI_API_KEY not set")

    gender_term = "men" if gender.lower() in ["male", "man", "masculino"] else "women"
    query = f"{gender_term} outfit for {event_type} in {event_location} {event_date}"

    print("🔍 Google Images query:", query)

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params={
                "engine": "google_images",
                "q": query,
                "api_key": SERPAPI_API_KEY,
            },
            timeout=30,
        )

        print("🌐 SerpAPI status:", response.status_code)
        response.raise_for_status()

        data = response.json()
        print("📦 SerpAPI JSON keys:", data.keys())

        images = []
        for item in data.get("images_results", [])[:10]:
            images.append({
                "title": item.get("title"),
                "image_url": item.get("original"),
                "thumbnail": item.get("thumbnail"),
                "link": item.get("link"),
                "source": item.get("source"),
            })

        print(f"🖼️ Images found: {len(images)}")
        return json.dumps({"query": query, "results": images})

    except Exception as e:
        print("❌ ERROR in style_recommender_tool")
        print(e)
        raise


# =========================
# TRAVEL TOOL
# =========================
@tool
def travel_recommender_tool(
    gender: str,
    event_date: str,
    event_location: str,
    event_type: str,
) -> str:
    """Generate concise travel recommendations for the event location/date using ChatOpenAI.

    Use this tool when the user asks for where to stay, what to see, or how to plan a short trip
    around the specified event. The LLM crafts a brief, actionable set of travel tips tailored to
    the provided details.

    Args:
        gender: Passed through for context if style or safety considerations are relevant.
        event_date: Date text (e.g., "July 4th", "next weekend") to align tips with timing/season.
        event_location: Destination city/region/country to ground the recommendations.
        event_type: Occasion the trip is centered on (conference, wedding, concert, etc.).

    Returns:
        Text from `call_travel_llm` with concise recommendations (lodging areas, key sights, food,
        transit tips, and quick packing/weather notes when helpful).

    Notes:
        - Prefer this tool for travel logistics or local highlights; use style_recommender_tool
          when the user mainly wants outfit ideas.
        - Inputs can be partial; the model will still attempt sensible defaults.
    """

    print("\n✈️ [TRAVEL TOOL] called")
    print("Inputs:", gender, event_date, event_location, event_type)

    return call_travel_llm({
        "gender": gender,
        "event_date": event_date,
        "event_location": event_location,
        "event_type": event_type,
    })
