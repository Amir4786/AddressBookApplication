import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db

# Test database URL is an in-memory SQLite database
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory database and session for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Ensure all ORM models are imported before creating tables.
    # Otherwise, Base.metadata may not include all mapped classes.
    import src.models.address  # noqa: F401

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a TestClient with the DB dependency overridden."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_address_data():
    """Sample valid address data for testing"""
    return {
        "name": "John Doe",
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "latitude": 40.7128,
        "longitude": -74.0060
    }

@pytest.fixture
def invalid_address_data():
    """Sample invalid address data for testing"""
    return {
        "name": "Jane Smith",
        "street": "456 Oak Ave",
        "city": "Los Angeles",
        "country": "USA",
        "latitude": 91.0,  # Invalid latitude
        "longitude": -118.2437
    }