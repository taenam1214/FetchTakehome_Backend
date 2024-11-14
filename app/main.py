from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from fastapi import FastAPI
from app.controllers import receipt_controller

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

# Process receipts endpoint
@router.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = str(uuid.uuid4())
    # Assuming `calculate_points` is a function that calculates points for a receipt
    points = calculate_points(receipt)  
    receipts_db[receipt_id] = points
    return {"id": receipt_id}

# Get points endpoint
@router.get("/receipts/{id}/points")
async def get_points(id: str):
    if id in receipts_db:
        return {"points": receipts_db[id]}
    raise HTTPException(status_code=404, detail="Receipt not found")

# Example points calculation function (implement your logic here)
def calculate_points(receipt: Receipt) -> int:
    # Implement points calculation logic here
    return 100  # Example fixed points value for testing
