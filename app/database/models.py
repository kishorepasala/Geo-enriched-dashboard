from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.database import Base
from datetime import datetime
from sqlalchemy import UniqueConstraint

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable = False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

class EnrichedLocation(Base):
    __tablename__ = "enriched_location"
    __table_args__ = (
        UniqueConstraint("address", "latitude", "longitude", name="unique_location"),
        {"extend_existing": True}
    )

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    # Weather data
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)

    # Air quality data
    aqi = Column(Float)
    pm10 = Column(Float)
    pm2_5 = Column(Float)
    co = Column(Float)
    no2 = Column(Float)
    so2 = Column(Float)
    o3 = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)