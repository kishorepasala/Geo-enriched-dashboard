import requests
from datetime import datetime

def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    response = requests.get(url, params = params)
    if response.status_code == 200:
        data = response.json().get("current_weather", {})
        return{
            "temperature": data.get("temperature"),
            "windspeed": data.get("windspeed"),
            "timezone": data.get("timezone"),
            "time": data.get("time")
        }
    else:
        return {
            "temperature": None,
            "windspeed": None,
            "timezone": None,
            "time": None
        }


def enrich_with_weather(geocoded_data):
    enriched = []
    for entry in geocoded_data:
        lat, lon = entry.get("latitude"), entry.get("longitude")
        if lat is not None and lon is not None:
            weather = get_weather(lat, lon)
            entry.update(weather)
        else:
            entry.update({
                "temperature": None,
                "windspeed": None,
                "timezone": None,
                "time": None
            })
        enriched.append(entry)
    return enriched

def fetch_weather(lat: float, lon: float):
    """
    Fetch current weather data for given coordinates using Open-Meteo API.
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data.get("current", {})
        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "precipitation": current.get("precipitation"),
            "wind_speed": current.get("wind_speed_10m"),
            "timestamp": current.get("time", datetime.utcnow().isoformat()),
        }
    except Exception as e:
        print(f"Error fetching weather for {lat}, {lon}: {e}")
        return None
