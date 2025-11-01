import requests

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
