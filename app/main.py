from fastapi import FastAPI
from app.api.routes import router
from app.database.database import engine, Base
from app.database import models

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="Geo-Enrichment DashBoard API")

# Include routes
app.include_router(router)

@app.get("/")
def root():
    return {"message":"Geo Enrichment DashBoard API is running"}
