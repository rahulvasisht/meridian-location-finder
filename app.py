from fastapi import FastAPI
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, SessionLocal

# Create database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Live Location API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Live Location API Running Successfully"
    }


@app.post("/send-location")
def send_location(location: schemas.LocationCreate):

    db: Session = SessionLocal()

    new_location = models.Location(
        latitude=location.latitude,
        longitude=location.longitude
    )

    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    db.close()

    return {
        "status": "success",
        "message": "Location saved successfully"
    }


@app.get("/get-location")
def get_location():

    db: Session = SessionLocal()

    latest_location = (
        db.query(models.Location)
        .order_by(models.Location.id.desc())
        .first()
    )

    db.close()

    if latest_location is None:
        return {
            "message": "No location found"
        }

    return {
        "latitude": latest_location.latitude,
        "longitude": latest_location.longitude,
        "time": latest_location.created_at
    }