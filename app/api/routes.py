from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import EnrichedLocation

router = APIRouter(prefix="/enriched-locations", tags=["Enriched Locations"])

@router.get("/")
def get_enriched_locations(db: Session = Depends(get_db)):
    data = db.query(EnrichedLocation).all()
    return data
