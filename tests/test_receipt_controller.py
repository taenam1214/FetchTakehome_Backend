from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_process_receipt_minimal_data():
    response = client.post("/receipts/process", json={
        "retailer": "A",
        "purchaseDate": "2023-12-01",
        "purchaseTime": "15:00",
        "items": [
            {"shortDescription": "Water", "price": "1.00"}
        ],
        "total": "1.00"
    })
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert isinstance(response_json["id"], str)

def test_process_receipt_round_dollar_total():
    response = client.post("/receipts/process", json={
        "retailer": "Retailer",
        "purchaseDate": "2023-03-15",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Item1", "price": "10.00"},
            {"shortDescription": "Item2", "price": "5.00"}
        ],
        "total": "15.00"
    })
    assert response.status_code == 200
    receipt_id = response.json()["id"]
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    assert points_response.json()["points"] > 50  # Should include 50 points for round dollar total

def test_get_points_invalid_format_id():
    # Test with an invalid format for receipt ID
    response = client.get("/receipts/invalid_id_format/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}

def test_process_receipt_multiple_of_quarter_total():
    response = client.post("/receipts/process", json={
        "retailer": "TestStore",
        "purchaseDate": "2022-05-01",
        "purchaseTime": "16:15",
        "items": [
            {"shortDescription": "ProductA", "price": "3.25"},
            {"shortDescription": "ProductB", "price": "6.75"}
        ],
        "total": "10.00"
    })
    assert response.status_code == 200
    receipt_id = response.json()["id"]
    points_response = client.get(f"/receipts/{receipt_id}/points")
    assert points_response.status_code == 200
    points = points_response.json()["points"]
    assert points >= 70, f"Expected at least 70 points, but got {points}"

def test_get_points_after_receipt_deletion():
    # Post a new receipt
    response = client.post("/receipts/process", json={
        "retailer": "Grocery",
        "purchaseDate": "2022-06-21",
        "purchaseTime": "15:45",
        "items": [
            {"shortDescription": "Milk", "price": "2.00"},
            {"shortDescription": "Bread", "price": "3.00"}
        ],
        "total": "5.00"
    })
    receipt_id = response.json()["id"]

    # Test with a non-existent UUID
    non_existent_id = str(uuid.uuid4())
    points_response = client.get(f"/receipts/{non_existent_id}/points")
    assert points_response.status_code == 404
    assert points_response.json() == {"detail": "Receipt not found"}

def test_get_points_non_existent_receipt():
    # Use a random UUID to test missing receipt ID without modifying receipts_data
    random_id = str(uuid.uuid4())
    response = client.get(f"/receipts/{random_id}/points")
    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}