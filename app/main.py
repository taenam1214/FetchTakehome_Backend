from fastapi import APIRouter, HTTPException, FastAPI
from pydantic import BaseModel
from app.controllers import receipt_controller

import uuid
import math
from datetime import datetime

app = FastAPI()
app.include_router(receipt_controller.router)
# In-memory storage for receipts
receipts_db = {}

router = APIRouter()

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: list[Item]
    total: str

# Include the router
app.include_router(router)

# Endpoint to process receipts and calculate points
@router.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts_db[receipt_id] = points
    return {"id": receipt_id}

# Endpoint to retrieve points by receipt ID
@router.get("/receipts/{id}/points")
async def get_points(id: str):
    if id in receipts_db:
        return {"points": receipts_db[id]}
    raise HTTPException(status_code=404, detail="Receipt not found")

# Function to calculate points based on receipt data
def calculate_points(receipt: Receipt) -> int:
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points += sum(1 for c in receipt.retailer if c.isalnum())

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    total_float = float(receipt.total)
    if total_float.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if (total_float * 100) % 25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt.
    points += (len(receipt.items) // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer
    for item in receipt.items:
        description_length = len(item.shortDescription.strip())
        if description_length % 3 == 0:
            price_points = math.ceil(float(item.price) * 0.2)
            points += price_points

    # Rule 6: 6 points if the day in the purchase date is odd.
    purchase_date = datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00 pm and before 4:00 pm.
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if purchase_time.hour == 14 or (purchase_time.hour == 15 and purchase_time.minute == 0):
        points += 10

    return points
