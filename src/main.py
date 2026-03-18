from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import Base, engine
from api.address import router as address_routes
from core.exceptions import AddressNotFoundException
from core.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(address_routes.router)


@app.exception_handler(AddressNotFoundException)
async def not_found_handler(request: Request, exc: AddressNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": f"Address {exc.address_id} not found"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )