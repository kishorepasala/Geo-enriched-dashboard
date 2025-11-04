import requests

def fetch_air_quality(lat, lon):
    # Try OpenAQ first (real sensor data)
    openaq_url = f"https://api.openaq.org/v2/latest?coordinates={lat},{lon}&radius=10000&limit=1"
    try:
        r = requests.get(openaq_url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data.get("results"):
            measurements = data["results"][0].get("measurements", [])
            aq_data = {m["parameter"]: m["value"] for m in measurements if "parameter" in m}
            return {
                "aqi": aq_data.get("pm2.5") or aq_data.get("pm10"),
                "pm10": aq_data.get("pm10"),
                "pm2_5": aq_data.get("pm2.5"),
                "co": aq_data.get("co"),
                "no2": aq_data.get("no2"),
                "so2": aq_data.get("so2"),
                "o3": aq_data.get("o3")
            }
    except Exception:
        pass

    # Fallback: Open-Meteo global air quality model
    try:
        url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=european_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        current = data.get("current", {})
        return {
            "aqi": current.get("european_aqi"),
            "pm10": current.get("pm10"),
            "pm2_5": current.get("pm2_5"),
            "co": current.get("carbon_monoxide"),
            "no2": current.get("nitrogen_dioxide"),
            "so2": current.get("sulphur_dioxide"),
            "o3": current.get("ozone")
        }
    except Exception:
        return {}
