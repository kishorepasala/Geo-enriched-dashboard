from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class EnrichedLocation(Base):
    __tablename__ = "enriched_location"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    windspeed = Column(Float)
    time = Column(String)

