import csv
from pathlib import Path
from app.services.geocode_service import batch_geocode
from app.services.weather_service import enrich_with_weather
from app.database.database import SessionLocal
from app.database.models import EnrichedLocation
from app.services.air_quality_service import fetch_air_quality
from app.services.weather_service import fetch_weather



def run_pipeline():
    csv_path = Path("data/input_addresses.csv")
    if not csv_path.exists():
        print("❌ input_addresses.csv not found.")
        return

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        addresses = [row["address"] for row in reader if row.get("address")]

    if not addresses:
        print("⚠️ No addresses found in CSV.")
        return

    print(f"🔍 Found {len(addresses)} addresses. Starting enrichment...")

    geocoded = batch_geocode(addresses)
    enriched = enrich_with_weather(geocoded)
    session = SessionLocal()

    for item in enriched:
        air = fetch_air_quality(item["latitude"], item["longitude"])
        weather = fetch_weather(item["latitude"], item["longitude"])
        entry = EnrichedLocation(
            address=item["address"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            temperature=weather.get("temperature"),
            humidity=weather.get("humidity"),
            wind_speed=weather.get("windspeed"),
            aqi=air.get("aqi"),
            pm10=air.get("pm10"),
            pm2_5=air.get("pm2_5"),
            co=air.get("co"),
            no2=air.get("no2"),
            so2=air.get("so2"),
            o3=air.get("o3"),
        )
        session.add(entry)
        print(f"✅ Saved: {item['address']}")
    session.commit()
    session.close()

    print("🚀 Pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
