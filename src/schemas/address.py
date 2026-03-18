from pydantic import BaseModel, field_validator

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
            raise ValueError("Invalid latitude")
        return v

    @field_validator("longitude")
    def validate_lon(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Invalid longitude")
        return v


class AddressResponse(AddressCreate):
    id: int

    class Config:
        from_attributes = True