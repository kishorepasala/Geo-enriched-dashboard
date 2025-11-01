import requests
import time

def geocode_address(address):
    """Fetch Latitude and Longitude from address."""
    url = "https://geocode.maps.co/search"
    params = {
        "q":address,
        "format": "json",
        "limit":1,
    }

    response = requests.get(url, params=params, headers={"User-Agent": "GeoEnrichmentDashboard"})
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return{
            "address": address,
            "latitude": float(data["lat"]),
            "longitude": float(data["lon"])
        }
    else:
        return {
            "address": address,
            "latitude": None,
            "longitude": None
        }


def batch_geocode(addresses):
    results = []
    for address in addresses:
        geo = geocode_address(address)
        results.append(geo)
        time.sleep(1)
    return results