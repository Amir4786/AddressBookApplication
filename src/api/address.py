from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.address import AddressCreate
from ..crud import address as crud
from ..core.exceptions import AddressNotFoundException
from ..core.logger import api_logger

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/")
def create(data: AddressCreate, db: Session = Depends(get_db)):
    try:
        address = crud.create_address(db, data)
        return address
    except ValidationError as e:
        api_logger.warning(f"Validation error creating address: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except Exception as e:
        api_logger.error(f"Failed to create address: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create address")


@router.put("/{id}")
def update(id: int, data: AddressCreate, db: Session = Depends(get_db)):
    try:
        address = crud.update_address(db, id, data)
        return address
    except ValidationError as e:
        api_logger.warning(f"Validation error updating address ID {id}: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except AddressNotFoundException:
        # Let the global exception handler return a consistent 404
        raise
    except Exception as e:
        api_logger.error(f"Failed to update address ID {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update address")


@router.get("/")
def read_all(db: Session = Depends(get_db)):
    try:
        addresses = crud.get_all_addresses(db)
        return addresses
    except Exception as e:
        api_logger.error(f"Failed to fetch all addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch addresses")


@router.get("/{id}")
def read_one(id: int, db: Session = Depends(get_db)):
    try:
        address = crud.get_address(db, id)
        return address
    except AddressNotFoundException:
        raise
    except Exception as e:
        api_logger.error(f"Failed to fetch address ID {id}: {str(e)}")
        raise


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    try:
        address = crud.delete_address(db, id)
        return {"message": f"Address {id} deleted"}
    except AddressNotFoundException:
        raise
    except Exception as e:
        api_logger.error(f"Failed to delete address ID {id}: {str(e)}")
        raise


@router.get("/nearby/")
def nearby(lat: float, lon: float, distance_km: float, db: Session = Depends(get_db)):
    try:
        # Validate inputs
        if not (-90 <= lat <= 90):
            api_logger.warning(f"Invalid latitude provided: {lat}")
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            api_logger.warning(f"Invalid longitude provided: {lon}")
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        if distance_km <= 0:
            api_logger.warning(f"Invalid distance provided: {distance_km}")
            raise HTTPException(status_code=400, detail="Distance must be positive")

        api_logger.info(f"Finding addresses near lat={lat}, lon={lon}, distance={distance_km}km")
        addresses = crud.get_nearby(db, lat, lon, distance_km)
        api_logger.info(f"Found {len(addresses)} addresses within {distance_km}km")
        return addresses
    except HTTPException:
        raise
    except Exception as e:
        api_logger.error(f"Failed to find nearby addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to find nearby addresses")