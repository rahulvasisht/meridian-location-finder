from pydantic import BaseModel


class LocationCreate(BaseModel):
    latitude: float
    longitude: float