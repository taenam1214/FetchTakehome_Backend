from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_process_receipt():
    response = client.post("/receipts/process", json={
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ],
        "total": "9.00"
    })
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert isinstance(response_json["id"], str)

def test_get_points():
    # First, create a receipt
    response = client.post("/receipts/process", json={
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"}
        ],
        "total": "9.00"
    })
    receipt_id = response.json()["id"]

    # Then, retrieve the points
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert "points" in points_response.json()
    assert isinstance(points_response.json()["points"], int)

def test_get_points_invalid_id():
    # Use a random UUID to test invalid receipt ID
    random_id = str(uuid.uuid4())
    response = client.get(f"/receipts/{random_id}/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}
