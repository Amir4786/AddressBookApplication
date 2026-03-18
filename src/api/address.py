from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.address import AddressCreate
from crud import address as crud

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/")
def create(data: AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db, data)


@router.get("/")
def read_all(db: Session = Depends(get_db)):
    return crud.get_all_addresses(db)


@router.get("/{id}")
def read_one(id: int, db: Session = Depends(get_db)):
    return crud.get_address(db, id)


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    return crud.delete_address(db, id)


@router.get("/nearby/")
def nearby(lat: float, lon: float, distance_km: float, db: Session = Depends(get_db)):
    return crud.get_nearby(db, lat, lon, distance_km)