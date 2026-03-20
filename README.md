# Address Book API

A modern, fast, and reliable REST API for managing addresses built with FastAPI and SQLAlchemy. Perfect for applications that need to store and query geographic location data.

## Features

- 🚀 **FastAPI**: High-performance async web framework
- 🗺️ **Geocoding & Routing**: Automatic coordinate lookup via GeoPy and TSP route planning
- 📍 **Geographic Support**: Store latitude/longitude coordinates with validation
- 🔍 **Nearby Search**: Find addresses within a specified radius using geodesic distance
- 📊 **SQLite Database**: Simple, file-based database (easy to set up)
- 📝 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- ✅ **Input Validation**: Pydantic models with proper data validation
- 🛡️ **Error Handling**: Proper HTTP status codes and error responses

## Project Structure

```
AddressBookApplication/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models/
│   │   └── address.py       # SQLAlchemy models
│   ├── schemas/
│   │   └── address.py       # Pydantic schemas
│   ├── crud/
│   │   └── address.py       # Database operations
│   ├── api/
│   │   └── address.py       # API endpoints
│   └── core/
│       ├── logger.py        # Logging configuration
│       └── exceptions.py    # Custom exceptions
├── logs/                    # Application logs (created automatically)
├── addresses.db             # SQLite database (created automatically)
├── requirements.txt         # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

### Windows

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AddressBookApplication
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Linux/Mac

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AddressBookApplication
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the server**
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Open your browser**
   - API Documentation: http://127.0.0.1:8000/docs
   - Alternative Docs: http://127.0.0.1:8000/redoc
   - Root endpoint: http://127.0.0.1:8000/

The server will start on `http://127.0.0.1:8000` and automatically reload when you make code changes.

## API Endpoints

### Addresses

- `GET /` - Health check endpoint
- `POST /addresses/` - Create a new address
- `GET /addresses/` - Get all addresses
- `GET /addresses/{id}` - Get address by ID
- `PUT /addresses/{id}` - Update address by ID
- `DELETE /addresses/{id}` - Delete address by ID
- `GET /addresses/nearby/?lat={lat}&lon={lon}&distance_km={km}` - Find nearby addresses
- `POST /addresses/route/` - Get optimal route order for multiple addresses

### Request/Response Examples

**Create Address**
```bash
POST /addresses/
Content-Type: application/json

{
  "name": "John Doe",
  "street": "123 Main St",
  "city": "New York",
  "country": "USA"
}
# Note: latitude and longitude are optional. They are automatically geocoded if omitted!
```

**Find Nearby Addresses**
```bash
GET /addresses/nearby/?lat=40.7128&lon=-74.0060&distance_km=10
```

**Route Ordering**
```bash
POST /addresses/route/
Content-Type: application/json

{
  "start_id": 1,
  "destination_ids": [4, 7, 2]
}
```

## Data Models

### AddressCreate
```python
{
  "name": "string",        # Required
  "street": "string",      # Required
  "city": "string",        # Required
  "country": "string",     # Required
  "latitude": float,       # Optional, -90 to 90 (Auto-geocoded if omitted)
  "longitude": float       # Optional, -180 to 180 (Auto-geocoded if omitted)
}
```

### RouteRequest
```python
{
  "start_id": int,              # Required, ID of starting address
  "destination_ids": list[int]  # Required, list of address IDs to visit
}
```

### AddressResponse
```python
{
  "id": 1,
  "name": "John Doe",
  "street": "123 Main St",
  "city": "New York",
  "country": "USA",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

## Development

### Logs

Application logs are automatically created in the `logs/` directory:
- `logs/app.log` - All application logs
- Console output also shows logs

### Database

The app uses SQLite (`addresses.db`) which is created automatically when you first run the application. No additional database setup required!

### Testing the API

You can test the API using:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **curl commands**
- **Postman** or any HTTP client
- **Python requests**

Example curl command:
```bash
curl -X POST "http://127.0.0.1:8000/addresses/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "street": "123 Main St",
       "city": "New York",
       "country": "USA",
       "latitude": 40.7128,
       "longitude": -74.0060
     }'
```

## Troubleshooting

**Port already in use?**
```bash
# Use a different port
uvicorn src.main:app --reload --port 8001
```

**Permission errors on Windows?**
- Run your terminal/command prompt as Administrator
- Or use `python` instead of `python3`

**Import errors?**
- Make sure you're in the correct directory (`AddressBookApplication/`)
- Ensure your virtual environment is activated
- Try reinstalling requirements: `pip install -r requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Testing

The project includes comprehensive API tests using pytest.

### Running Tests

1. **Run all tests (recommended)**
   ```bash
   python run_tests.py
   ```

2. **Run pytest directly**
   ```bash
   python -m pytest -q
   ```

3. **Run a specific test**
   ```bash
   python run_tests.py -k test_create_address_success
   ```

4. **Run with coverage report**
   ```bash
   pip install pytest-cov
   python run_tests.py --cov=src --cov-report=html
   ```

### Test Coverage

The test suite covers:
- ✅ All API endpoints (GET, POST, PUT, DELETE)
- ✅ Input validation and error handling
- ✅ Database operations
- ✅ Geographic calculations
- ✅ Edge cases and error scenarios
- ✅ Integration tests

### Test Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_api.py          # API endpoint tests
└── run_tests.py         # Test runner script
```
