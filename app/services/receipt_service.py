import math

def calculate_points(receipt):
    points = 0
    points += points_for_retailer_name(receipt.retailer)
    points += points_for_total_amount(receipt.total)
    points += points_for_item_pairs(receipt.items)
    points += points_for_item_description(receipt.items)
    points += points_for_odd_day(receipt.purchaseDate)
    points += points_for_purchase_time(receipt.purchaseTime)
    return points

def points_for_retailer_name(retailer):
    return sum(1 for c in retailer if c.isalnum())

def points_for_total_amount(total):
    points = 0
    total_float = float(total)
    if total_float.is_integer():
        points += 50
    elif (total_float * 100) % 25 == 0:
        points += 25
    return points

def points_for_item_pairs(items):
    return (len(items) // 2) * 5

def points_for_item_description(items):
    points = 0
    for item in items:
        description_length = len(item.shortDescription.strip())
        print(f"Description: '{item.shortDescription.strip()}', Length: {description_length}")  # Debug
        if description_length % 3 == 0:
            price_points = math.ceil(float(item.price) * 0.2)
            print(f"Price: {item.price}, Points Awarded: {price_points}")  # Debug
            points += price_points
    return points

def points_for_odd_day(purchase_date):
    day = int(purchase_date.split("-")[2])
    return 6 if day % 2 == 1 else 0

def points_for_purchase_time(purchase_time):
    hour, minute = map(int, purchase_time.split(":"))
    return 10 if 14 <= hour < 16 else 0
