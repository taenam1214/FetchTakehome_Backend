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

def test_retailer_name_empty():
    points = points_for_retailer_name("")
    assert points == 0  # No alphanumeric characters

def test_retailer_name_special_characters():
    points = points_for_retailer_name("!!!@@@###")
    assert points == 0  # Special characters only, no alphanumeric

def test_total_exact_multiple_of_quarter():
    total_points = points_for_total_amount("9.25")
    assert total_points == 25  # Total is a multiple of 0.25

def test_total_round_dollar_and_multiple_of_quarter():
    total_points = points_for_total_amount("25.00")
    assert total_points == 50  # Only round dollar should apply, not both

def test_item_pairs_with_odd_number():
    items = [
        Item(shortDescription="Apple", price="1.00"),
        Item(shortDescription="Banana", price="1.00"),
        Item(shortDescription="Orange", price="1.00")
    ]
    points = points_for_item_pairs(items)
    assert points == 5  # Only one pair gives points

def test_item_description_points_multiple_of_three():
    items = [
        Item(shortDescription="Item12345678901", price="5.00")  # 15 characters (multiple of 3)
    ]
    points = points_for_item_description(items)
    assert points == 1, f"Expected 1 point, but got {points}"  # 5.00 * 0.2 = 1 point

def test_odd_day_points_even_day():
    points = points_for_odd_day("2023-12-02")  # Even day
    assert points == 0  # No points for even day

def test_purchase_time_out_of_range():
    points = points_for_purchase_time("10:00")
    assert points == 0  # No points for out-of-range time

def test_purchase_time_edge_cases():
    assert points_for_purchase_time("14:00") == 10  # Exactly 2:00 pm
    assert points_for_purchase_time("15:59") == 10  # Exactly 3:59 pm
    assert points_for_purchase_time("13:59") == 0   # One minute before 2:00 pm
    assert points_for_purchase_time("16:00") == 0   # Exactly 4:00 pm