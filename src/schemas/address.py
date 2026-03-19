from pydantic import BaseModel, field_validator
from ..core.logger import schema_logger

class AddressCreate(BaseModel):
    name: str
    street: str
    city: str
    country: str
    latitude: float
    longitude: float

    @field_validator("latitude")
    def validate_lat(cls, v):
        if not -90 <= v <= 90:
            schema_logger.warning(f"Invalid latitude provided: {v}")
            raise ValueError("Invalid latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def validate_lon(cls, v):
        if not -180 <= v <= 180:
            schema_logger.warning(f"Invalid longitude provided: {v}")
            raise ValueError("Invalid longitude must be between -180 and 180")
        return v


class AddressResponse(AddressCreate):
    id: int

    class Config:
        from_attributes = True