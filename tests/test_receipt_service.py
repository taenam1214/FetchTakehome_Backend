import pytest
from app.services.receipt_service import (
    calculate_points,
    points_for_retailer_name,
    points_for_total_amount,
    points_for_item_pairs,
    points_for_item_description,
    points_for_odd_day,
    points_for_purchase_time
)
from app.models.receipt import Receipt, Item

@pytest.fixture
def sample_receipt():
    return Receipt(
        retailer="Target",
        purchaseDate="2022-03-20",
        purchaseTime="14:33",
        items=[
            Item(shortDescription="Gatorade", price="2.25"),
            Item(shortDescription="Gatorade", price="2.25")
        ],
        total="9.00"
    )

def test_retailer_name_points(sample_receipt):
    sample_receipt.retailer = "Target"
    assert points_for_retailer_name(sample_receipt.retailer) == 6

def test_total_round_dollar_points(sample_receipt):
    sample_receipt.total = "50.00"
    assert points_for_total_amount(sample_receipt.total) == 50

def test_total_multiple_of_quarter(sample_receipt):
    sample_receipt.total = "9.25"
    assert points_for_total_amount(sample_receipt.total) == 25

def test_item_count_pairs(sample_receipt):
    sample_receipt.items.append(Item(shortDescription="Gatorade", price="2.25"))
    sample_receipt.items.append(Item(shortDescription="Gatorade", price="2.25"))
    assert points_for_item_pairs(sample_receipt.items) == 10  # 4 items, 2 pairs = 10 points

def test_item_description_length_multiple_of_three(sample_receipt):
    # Keep the description with the space included
    sample_receipt.items[0].shortDescription = "Mountain Dew 12PK"
    sample_receipt.items[0].price = "6.49"
    # Expect 0 points because 17 is not a multiple of 3
    assert points_for_item_description(sample_receipt.items) == 0

def test_odd_day_points(sample_receipt):
    sample_receipt.purchaseDate = "2022-01-01"
    assert points_for_odd_day(sample_receipt.purchaseDate) == 6

def test_purchase_time_bonus(sample_receipt):
    sample_receipt.purchaseTime = "14:30"
    assert points_for_purchase_time(sample_receipt.purchaseTime) == 10
