from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .database import Base, engine
from .api.address import router as address_routes
from .core.exceptions import AddressNotFoundException
from .core.logger import logger
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(address_routes)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Request started: {request.method} {request.url}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.3f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url} - Time: {process_time:.3f}s - Error: {str(e)}")
        raise


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Address Book API is running", "docs": "/docs"}


@app.exception_handler(AddressNotFoundException)
async def not_found_handler(request: Request, exc: AddressNotFoundException):
    logger.warning(f"Address not found - ID: {exc.address_id}, Method: {request.method}, URL: {request.url}")
    return JSONResponse(
        status_code=404,
        content={"error": f"Address {exc.address_id} not found"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception - Method: {request.method}, URL: {request.url}, Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# Startup logging
@app.on_event("startup")
async def startup_event():
    logger.info("Address Book API starting up")
    logger.info("Database tables created/verified")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Address Book API shutting down")