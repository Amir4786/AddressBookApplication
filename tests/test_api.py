import pytest
from fastapi.testclient import TestClient

# Test data
valid_address_data = {
    "name": "John Doe",
    "street": "123 Main St",
    "city": "New York",
    "country": "USA",
    "latitude": 40.7128,
    "longitude": -74.0060
}

invalid_address_data = {
    "name": "Jane Smith",
    "street": "456 Oak Ave",
    "city": "Los Angeles",
    "country": "USA",
    "latitude": 91.0,  # Invalid latitude (> 90)
    "longitude": -118.2437
}

def create_test_address(client, address_data=None):
    """Helper function to create a test address"""
    if address_data is None:
        address_data = valid_address_data
    response = client.post("/addresses/", json=address_data)
    return response

class TestRootEndpoint:
    """Test the root endpoint"""

    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["message"] == "Address Book API is running"
        assert data["docs"] == "/docs"

class TestCreateAddress:
    """Test address creation endpoints"""

    def test_create_address_success(self, client):
        response = create_test_address(client)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["street"] == "123 Main St"
        assert data["city"] == "New York"
        assert data["country"] == "USA"
        assert data["latitude"] == 40.7128
        assert data["longitude"] == -74.0060
        assert "id" in data

    def test_create_address_invalid_latitude(self, client):
        response = create_test_address(client, invalid_address_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_create_address_missing_required_field(self, client):
        incomplete_data = {
            "name": "Test User",
            "street": "123 Test St",
            # Missing city, country, latitude, longitude
        }
        response = client.post("/addresses/", json=incomplete_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_create_address_invalid_data_types(self, client):
        invalid_types_data = {
            "name": 123,  # Should be string
            "street": "123 Main St",
            "city": "New York",
            "country": "USA",
            "latitude": "40.7128",  # Should be number
            "longitude": -74.0060
        }
        response = client.post("/addresses/", json=invalid_types_data)
        assert response.status_code == 422

class TestGetAddresses:
    """Test address retrieval endpoints"""

    def test_get_all_addresses_empty(self, client):
        response = client.get("/addresses/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_all_addresses_with_data(self, client):
        # Create a test address first
        create_test_address(client)

        response = client.get("/addresses/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "John Doe"

    def test_get_address_by_id_success(self, client):
        # Create a test address first
        create_response = create_test_address(client)
        address_id = create_response.json()["id"]

        response = client.get(f"/addresses/{address_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == address_id
        assert data["name"] == "John Doe"

    def test_get_address_by_id_not_found(self, client):
        response = client.get("/addresses/999")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "not found" in data["error"].lower()

    def test_get_address_by_id_invalid_id(self, client):
        response = client.get("/addresses/invalid")
        assert response.status_code == 422  # FastAPI validation error

class TestUpdateAddress:
    """Test address update endpoints"""

    def test_update_address_success(self, client):
        # Create a test address first
        create_response = create_test_address(client)
        address_id = create_response.json()["id"]

        update_data = {
            "name": "Jane Smith",
            "street": "456 Oak Ave",
            "city": "Los Angeles",
            "country": "USA",
            "latitude": 34.0522,
            "longitude": -118.2437
        }

        response = client.put(f"/addresses/{address_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == address_id
        assert data["name"] == "Jane Smith"
        assert data["city"] == "Los Angeles"

    def test_update_address_not_found(self, client):
        update_data = {
            "name": "Jane Smith",
            "street": "456 Oak Ave",
            "city": "Los Angeles",
            "country": "USA",
            "latitude": 34.0522,
            "longitude": -118.2437
        }

        response = client.put("/addresses/999", json=update_data)
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_update_address_invalid_data(self, client):
        # Create a test address first
        create_response = create_test_address(client)
        address_id = create_response.json()["id"]

        invalid_update_data = {
            "name": "Jane Smith",
            "street": "456 Oak Ave",
            "city": "Los Angeles",
            "country": "USA",
            "latitude": 91.0,  # Invalid latitude
            "longitude": -118.2437
        }

        response = client.put(f"/addresses/{address_id}", json=invalid_update_data)
        assert response.status_code == 422

class TestDeleteAddress:
    """Test address deletion endpoints"""

    def test_delete_address_success(self, client):
        # Create a test address first
        create_response = create_test_address(client)
        address_id = create_response.json()["id"]

        response = client.delete(f"/addresses/{address_id}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Address {address_id} deleted" in data["message"]

        # Verify it's actually deleted
        get_response = client.get(f"/addresses/{address_id}")
        assert get_response.status_code == 404

    def test_delete_address_not_found(self, client):
        response = client.delete("/addresses/999")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

class TestNearbyAddresses:
    """Test nearby addresses endpoint"""

    def test_nearby_addresses_success(self, client):
        # Create test addresses
        addresses_data = [
            {
                "name": "Address 1",
                "street": "123 Main St",
                "city": "New York",
                "country": "USA",
                "latitude": 40.7128,
                "longitude": -74.0060
            },
            {
                "name": "Address 2",
                "street": "456 Oak Ave",
                "city": "Newark",
                "country": "USA",
                "latitude": 40.7357,
                "longitude": -74.1724
            },
            {
                "name": "Address 3",
                "street": "789 Pine St",
                "city": "Philadelphia",
                "country": "USA",
                "latitude": 39.9526,
                "longitude": -75.1652
            }
        ]

        for addr_data in addresses_data:
            create_test_address(client, addr_data)

        # Search for addresses near New York within 50km
        response = client.get("/addresses/nearby/?lat=40.7128&lon=-74.0060&distance_km=50")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should find at least the New York and Newark addresses
        assert len(data) >= 2

        # Check that each result has distance
        for addr in data:
            assert "distance" in addr
            assert isinstance(addr["distance"], (int, float))

    def test_nearby_addresses_invalid_latitude(self, client):
        response = client.get("/addresses/nearby/?lat=91&lon=-74.0060&distance_km=10")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "latitude" in data["detail"].lower()

    def test_nearby_addresses_invalid_longitude(self, client):
        response = client.get("/addresses/nearby/?lat=40.7128&lon=-200&distance_km=10")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "longitude" in data["detail"].lower()

    def test_nearby_addresses_invalid_distance(self, client):
        response = client.get("/addresses/nearby/?lat=40.7128&lon=-74.0060&distance_km=-5")
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "distance" in data["detail"].lower()

    def test_nearby_addresses_missing_parameters(self, client):
        response = client.get("/addresses/nearby/")
        assert response.status_code == 422  # Missing required query parameters

    def test_nearby_addresses_no_results(self, client):
        # Search in a remote location
        response = client.get("/addresses/nearby/?lat=0&lon=0&distance_km=1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should be empty or very few results
        assert len(data) == 0

class TestIntegration:
    """Integration tests for multiple operations"""

    def test_full_crud_cycle(self, client):
        # Create
        create_response = create_test_address(client)
        assert create_response.status_code == 200
        address_id = create_response.json()["id"]

        # Read
        get_response = client.get(f"/addresses/{address_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "John Doe"

        # Update
        update_data = {
            "name": "Updated Name",
            "street": "Updated Street",
            "city": "Updated City",
            "country": "Updated Country",
            "latitude": 41.0,
            "longitude": -75.0
        }
        update_response = client.put(f"/addresses/{address_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Name"

        # Delete
        delete_response = client.delete(f"/addresses/{address_id}")
        assert delete_response.status_code == 200

        # Verify deletion
        final_get_response = client.get(f"/addresses/{address_id}")
        assert final_get_response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__])