# planner_pipeline.py
from typing import Dict, Any
from datetime import datetime
from tools import find_pois_osm, get_weather_open_meteo, POIToolError, WeatherToolError
from utils import parse_trip_sentence
from agents import create_itinerary_from_state

def plan_trip_structured(city: str, start_date: str, end_date: str, preferences: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Fixed pipeline: POIs -> Weather -> Itinerary.
    Returns a dict with keys: pois, weather, itinerary, meta.
    """
    preferences = preferences or {}
    state: Dict[str, Any] = {"tools_called": [], "errors": []}

    # POIs
    try:
        pois = find_pois_osm(city, limit=12)
        state["pois"] = pois
        state["tools_called"].append({"tool": "POI_TOOL", "result": f"{len(pois.get('pois', []))} pois"})
    except POIToolError as e:
        state["errors"].append(f"POI_TOOL error: {e}")
        pois = {"city": city, "center": {"lat": 0.0, "lon": 0.0}, "pois": []}
        state["pois"] = pois

    # Weather
    try:
        center = state["pois"].get("center", {})
        lat = float(center.get("lat", 0.0))
        lon = float(center.get("lon", 0.0))
        weather = get_weather_open_meteo(lat, lon, start_date, end_date)
        state["weather"] = weather
        state["tools_called"].append({"tool": "WEATHER_TOOL", "result": f"{len(weather.get('daily', []))} days"})
    except WeatherToolError as e:
        state["errors"].append(f"WEATHER_TOOL error: {e}")
        state["weather"] = {"latitude": 0.0, "longitude": 0.0, "daily": []}

    # Itinerary (reuse your existing helper)
    itinerary = create_itinerary_from_state(state, start_date, end_date, preferences)
    state["itinerary"] = itinerary
    state["tools_called"].append({"tool": "ITINERARY_CREATOR", "result": f"{len(itinerary.get('days', []))} days"})

    return {
        "pois": state.get("pois"),
        "weather": state.get("weather"),
        "itinerary": state.get("itinerary"),
        "meta": {
            "tools_called": state.get("tools_called", []),
            "errors": state.get("errors", []),
        },
    }

def plan_trip_nl(query: str) -> Dict[str, Any]:
    """Natural-language entrypoint using existing parse_trip_sentence()."""
    parsed = parse_trip_sentence(query)
    city = parsed["city"]
    start_date = parsed["start_date"]
    end_date = parsed["end_date"]
    prefs = parsed.get("preferences", {})
    return plan_trip_structured(city, start_date, end_date, prefs)
