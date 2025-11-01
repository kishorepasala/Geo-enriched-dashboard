from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///geo_data.db"

engine = create_engine(DATABASE_URL, echo = False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for FastApi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()