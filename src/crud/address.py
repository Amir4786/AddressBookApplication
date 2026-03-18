from sqlalchemy.orm import Session
from models.address_model import Address
from schemas.address_schema import AddressCreate
from core.logger import logger
from core.exceptions import AddressNotFoundException
from math import radians, cos, sin, acos


def create_address(db: Session, data: AddressCreate):
    try:
        address = Address(**data.dict())
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating address: {e}")
        raise


def get_all_addresses(db: Session):
    return db.query(Address).all()


def get_address(db: Session, address_id: int):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise AddressNotFoundException(address_id)
    return address


def delete_address(db: Session, address_id: int):
    address = get_address(db, address_id)
    db.delete(address)
    db.commit()
    return address


def get_nearby(db: Session, lat: float, lon: float, distance_km: float):
    addresses = db.query(Address).all()
    result = []

    for addr in addresses:
        distance = 6371 * acos(
            cos(radians(lat)) * cos(radians(addr.latitude)) *
            cos(radians(addr.longitude) - radians(lon)) +
            sin(radians(lat)) * sin(radians(addr.latitude))
        )

        if distance <= distance_km:
            result.append({**addr.__dict__, "distance": distance})

    return result