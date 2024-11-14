from fastapi import APIRouter, HTTPException
from app.models.receipt import Receipt
from app.services.receipt_service import calculate_points
from app.utils.id_generator import generate_id

router = APIRouter()
receipts_data = {}

@router.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    receipt_id = generate_id()
    points = calculate_points(receipt)
    receipts_data[receipt_id] = points
    return {"id": receipt_id}

@router.get("/receipts/{id}/points")
async def get_points(id: str):
    points = receipts_data.get(id)
    if points is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return {"points": points}
