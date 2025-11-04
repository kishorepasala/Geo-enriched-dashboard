import pandas as pd
from fastapi import UploadFile
from app.database.database import SessionLocal
from app.database import models
from io import StringIO

def process_and_store_file(file: UploadFile):
    try:
        contents = file.file.read().decode("utf-8")
        df = pd.read_csv(StringIO(contents))
        df.columns = [col.strip().lower() for col in df.columns]

        required_columns = {"address", "latitude", "longitude"}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Missing required columns: {required_columns}")

        db = SessionLocal()
        for _,row in df.iterrows():
            record = models.Address(
                address=row["address"],
                latitude=row["latitude"],
            )
            db.add(record)
        db.commit()
        db.close()

        return {"status": "success", "records_inserted":len(df)}
    except Exception as e:
        return {"status": "error", "message>": str(e)}