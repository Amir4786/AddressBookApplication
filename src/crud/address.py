from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models.address import Address
from ..schemas.address import AddressCreate
from ..core.logger import crud_logger
from ..core.exceptions import AddressNotFoundException
from math import radians, cos, sin, acos


def create_address(db: Session, data: AddressCreate):
    crud_logger.info(f"Creating address: {data.name} - {data.street}, {data.city}, {data.country}")
    try:
        address = Address(**data.dict())
        db.add(address)
        db.commit()
        db.refresh(address)
        crud_logger.info(f"Address created successfully with ID: {address.id}")
        return address
    except IntegrityError as e:
        db.rollback()
        crud_logger.error(f"Database integrity error creating address: {e}")
        raise ValueError("Address data conflicts with existing records")
    except SQLAlchemyError as e:
        db.rollback()
        crud_logger.error(f"Database error creating address: {e}")
        raise
    except Exception as e:
        db.rollback()
        crud_logger.error(f"Unexpected error creating address: {e}")
        raise


def update_address(db: Session, id: int, data: AddressCreate):
    crud_logger.info(f"Updating address ID: {id} with data: {data.name} - {data.street}, {data.city}")
    try:
        address = db.query(Address).filter(Address.id == id).first()
        if not address:
            crud_logger.warning(f"Address ID {id} not found for update")
            raise AddressNotFoundException(id)
        for key, value in data.dict().items():
            setattr(address, key, value)
        db.commit()
        db.refresh(address)
        crud_logger.info(f"Address ID {id} updated successfully")
        return address
    except AddressNotFoundException:
        raise
    except IntegrityError as e:
        db.rollback()
        crud_logger.error(f"Database integrity error updating address ID {id}: {e}")
        raise ValueError("Address data conflicts with existing records")
    except SQLAlchemyError as e:
        db.rollback()
        crud_logger.error(f"Database error updating address ID {id}: {e}")
        raise
    except Exception as e:
        db.rollback()
        crud_logger.error(f"Unexpected error updating address ID {id}: {e}")
        raise


def get_all_addresses(db: Session):
    crud_logger.debug("Querying all addresses from database")
    try:
        addresses = db.query(Address).all()
        crud_logger.info(f"Retrieved {len(addresses)} addresses from database")
        return addresses
    except SQLAlchemyError as e:
        crud_logger.error(f"Database error fetching all addresses: {e}")
        raise
    except Exception as e:
        crud_logger.error(f"Unexpected error fetching all addresses: {e}")
        raise


def get_address(db: Session, address_id: int):
    crud_logger.debug(f"Querying address ID: {address_id}")
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            crud_logger.warning(f"Address ID {address_id} not found")
            raise AddressNotFoundException(address_id)
        crud_logger.debug(f"Address ID {address_id} found")
        return address
    except SQLAlchemyError as e:
        crud_logger.error(f"Database error fetching address ID {address_id}: {e}")
        raise
    except Exception as e:
        crud_logger.error(f"Unexpected error fetching address ID {address_id}: {e}")
        raise


def delete_address(db: Session, address_id: int):
    crud_logger.info(f"Deleting address ID: {address_id}")
    try:
        address = get_address(db, address_id)  # This will raise if not found
        db.delete(address)
        db.commit()
        crud_logger.info(f"Address ID {address_id} deleted successfully")
        return address
    except AddressNotFoundException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        crud_logger.error(f"Database error deleting address ID {address_id}: {e}")
        raise
    except Exception as e:
        db.rollback()
        crud_logger.error(f"Unexpected error deleting address ID {address_id}: {e}")
        raise


def get_nearby(db: Session, lat: float, lon: float, distance_km: float):
    crud_logger.debug(f"Finding addresses near lat={lat}, lon={lon} within {distance_km}km")
    try:
        addresses = db.query(Address).all()
        result = []

        for addr in addresses:
            try:
                distance = 6371 * acos(
                    cos(radians(lat)) * cos(radians(addr.latitude)) *
                    cos(radians(addr.longitude) - radians(lon)) +
                    sin(radians(lat)) * sin(radians(addr.latitude))
                )

                if distance <= distance_km:
                    result.append({**addr.__dict__, "distance": distance})
            except (ValueError, TypeError, ZeroDivisionError) as e:
                crud_logger.warning(f"Error calculating distance for address ID {addr.id}: {e}")
                continue
            except Exception as e:
                crud_logger.error(f"Unexpected error calculating distance for address ID {addr.id}: {e}")
                continue

        crud_logger.info(f"Found {len(result)} addresses within {distance_km}km of ({lat}, {lon})")
        return result
    except SQLAlchemyError as e:
        crud_logger.error(f"Database error finding nearby addresses: {e}")
        raise
    except Exception as e:
        crud_logger.error(f"Unexpected error finding nearby addresses: {e}")
        raise