from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models


router = APIRouter()

# 1. Get all enriched locations
@router.get("/locations")
def get_all_locations(db: Session = Depends(get_db)):
    locations = db.query(models.EnrichedLocation).all()
    if not locations:
        raise HTTPException(status_code=404, detail="Location not found")
    return locations

# Get location details by city
@router.get("/locations/{city}")
def get_location(city: str, db: Session = Depends(get_db)):
    location = (
        db.query(models.EnrichedLocation)
        .filter(models.EnrichedLocation.address.ilike(f"%{city}"))
        .first()
    )
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

# 3. Get basic weather statistics (avg temp, avg wind)
@router.get("/stats")
def get_weather_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func

    stats = (
        db.query(
            func.avg(models.EnrichedLocation.temperature).label("avg_temperature"),
            func.avg(models.EnrichedLocation.windspeed).label("avg_wind"),
        )
        .first()
    )
    return {
        "average_temperature": round(stats.avg_temperature, 2) if stats.avg_temperature else None,
        "average_wind": round(stats.avg_wind, 2) if stats.avg_wind else None,
    }
