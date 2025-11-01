import csv
from pathlib import Path
from app.services.geocode_service import batch_geocode
from app.services.weather_service import enrich_with_weather
from app.database.database import SessionLocal
from app.database.models import EnrichedLocation

def load_addresses(file_path: str):
    """Read the input CSV file and returns a list of addresses"""
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    addresses = []
    with open(file_path, mode='r', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            address = row.get("address")
            if address and address.strip():
                addresses.append(address.strip())

    return addresses



def save_to_database(data):
    session = SessionLocal()
    try:
        for entry in data:
            record = EnrichedLocation(
                address=entry["address"],
                latitude=entry["latitude"],
                longitude=entry["longitude"],
                temperature=entry["temperature"],
                windspeed=entry["windspeed"],
                time=entry["time"]
            )
            session.add(record)
        session.commit()
        print("Data saved to database")
    except Exception as e:
        session.rollback()
        print("Error saving data to database: ", e)
    finally:
        session.close()


if __name__ == "__main__":
    input_path = "/Users/kishore/PythonProject/PythonProject/PythonProject/Geo enriched dashboard/data/input_addresses.csv"
    addresses = load_addresses(input_path)
    print("Loaded addresses: {addresses}")

    geocoded_data = batch_geocode(addresses)
    print("Geocoded Data: ", geocoded_data)

    enriched_data = enrich_with_weather(geocoded_data)
    print("Weather Enriched Data: ", enriched_data)

    save_to_database(enriched_data)





