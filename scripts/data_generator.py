import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

# =====================================================
# SETTINGS
# =====================================================
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_ORDERS = 20000

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

os.makedirs("data/raw", exist_ok=True)

# =====================================================
# HELPERS
# =====================================================
def weighted_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]

def get_month_weight(month: int) -> float:
    # Stronger retail seasonality
    # Nov = Black Friday, Dec = festive / year-end spending
    base = {
        1: 0.75, 2: 0.72, 3: 0.80, 4: 0.85,
        5: 0.88, 6: 0.90, 7: 0.92, 8: 0.95,
        9: 0.98, 10: 1.05, 11: 1.45, 12: 1.65
    }
    return base[month]

def get_day_weight(day: int) -> float:
    # Payday spikes: 25th to 30th/31st
    if day >= 25:
        return 1.35
    if day in [15, 16, 17]:
        return 1.12
    return 1.0

def generate_order_date():
    days = (END_DATE - START_DATE).days
    candidates = []
    weights = []

    for i in range(days + 1):
        date = START_DATE + timedelta(days=i)
        weight = get_month_weight(date.month) * get_day_weight(date.day)

        # Weekend boost
        if date.weekday() >= 5:
            weight *= 1.10

        # Black Friday / festive spike
        if date.month == 11 and 20 <= date.day <= 30:
            weight *= 1.60
        if date.month == 12 and 1 <= date.day <= 31:
            weight *= 1.35

        candidates.append(date)
        weights.append(weight)

    return weighted_choice(candidates, weights)

def region_preferences(region):
    # Category preference by region
    if region == "Johannesburg":
        return {
            "Electronics": 0.38, "Clothing": 0.22, "Groceries": 0.20, "Furniture": 0.20
        }
    if region == "Cape Town":
        return {
            "Clothing": 0.35, "Electronics": 0.22, "Groceries": 0.18, "Furniture": 0.25
        }
    if region == "Durban":
        return {
            "Groceries": 0.40, "Clothing": 0.25, "Electronics": 0.15, "Furniture": 0.20
        }
    if region == "Pretoria":
        return {
            "Furniture": 0.35, "Electronics": 0.25, "Clothing": 0.20, "Groceries": 0.20
        }
    return {
        "Electronics": 0.25, "Clothing": 0.25, "Groceries": 0.25, "Furniture": 0.25
    }

def segment_preferences(segment):
    # Payment and purchasing behavior by segment
    if segment == "Premium":
        return {"online": 0.45, "card": 0.45, "cash": 0.10}
    if segment == "Wholesale":
        return {"online": 0.20, "card": 0.35, "cash": 0.45}
    return {"online": 0.25, "card": 0.50, "cash": 0.25}

def discount_probability(month, category, segment):
    # More discounts in Black Friday / festive season
    p = 0.20
    if month == 11:
        p += 0.30
    if month == 12:
        p += 0.18

    # Category-specific promo behavior
    if category == "Clothing":
        p += 0.10
    if category == "Electronics":
        p += 0.08

    # Segment-specific discount sensitivity
    if segment == "Wholesale":
        p += 0.15
    if segment == "Premium":
        p -= 0.05

    return min(max(p, 0.05), 0.85)

def generate_discount(month, category, segment):
    p = discount_probability(month, category, segment)
    if random.random() > p:
        return 0.0

    if month == 11:
        return random.choice([0.10, 0.15, 0.20, 0.25, 0.30, 0.40])
    if month == 12:
        return random.choice([0.05, 0.10, 0.15, 0.20, 0.25])

    if category == "Clothing":
        return random.choice([0.05, 0.10, 0.15, 0.20])
    if category == "Electronics":
        return random.choice([0.05, 0.10, 0.15])
    if segment == "Wholesale":
        return random.choice([0.10, 0.15, 0.20, 0.25])
    return random.choice([0.05, 0.10, 0.15])

def generate_quantity(category, segment, month, discount):
    # Demand behavior by category, segment, season, and discount
    base_map = {
        "Groceries": [2, 3, 4, 5, 6, 7, 8],
        "Clothing": [1, 1, 2, 2, 3, 4, 5],
        "Electronics": [1, 1, 1, 2, 2, 3],
        "Furniture": [1, 1, 1, 1, 2]
    }

    qty = random.choice(base_map[category])

    if segment == "Premium":
        qty = max(1, qty - 1)
    if segment == "Wholesale":
        qty += random.choice([1, 2, 3])

    if month == 11:
        qty += random.choice([0, 1, 2])
    if month == 12:
        qty += random.choice([0, 1, 2])

    # Discount elasticity: bigger discounts increase quantity
    if discount >= 0.25:
        qty += 2
    elif discount >= 0.15:
        qty += 1

    return int(max(1, qty))

def category_price_ranges(category):
    if category == "Electronics":
        return (1200, 15000)
    if category == "Furniture":
        return (800, 12000)
    if category == "Clothing":
        return (80, 1500)
    if category == "Groceries":
        return (20, 600)
    return (50, 2000)

# =====================================================
# CUSTOMERS
# =====================================================
customer_segments = np.random.choice(
    ["Regular", "Premium", "Wholesale"],
    NUM_CUSTOMERS,
    p=[0.62, 0.28, 0.10]
)

customers = pd.DataFrame({
    "customer_id": range(1, NUM_CUSTOMERS + 1),
    "name": [f"Customer_{i}" for i in range(1, NUM_CUSTOMERS + 1)],
    "gender": np.random.choice(["Male", "Female"], NUM_CUSTOMERS, p=[0.48, 0.52]),
    "age": np.random.randint(18, 70, NUM_CUSTOMERS),
    "city": np.random.choice(
        ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Bloemfontein"],
        NUM_CUSTOMERS,
        p=[0.34, 0.22, 0.18, 0.16, 0.10]
    ),
    "segment": customer_segments
})

# =====================================================
# PRODUCTS
# =====================================================
categories = np.random.choice(
    ["Electronics", "Clothing", "Groceries", "Furniture"],
    NUM_PRODUCTS,
    p=[0.24, 0.30, 0.28, 0.18]
)

products = pd.DataFrame({
    "product_id": range(1, NUM_PRODUCTS + 1),
    "product_name": [f"Product_{i}" for i in range(1, NUM_PRODUCTS + 1)],
    "category": categories
})

subcats = []
cost_prices = []
selling_prices = []

for _, row in products.iterrows():
    cat = row["category"]
    subcats.append(f"{cat}_{random.choice(['A', 'B', 'C', 'D'])}")

    low, high = category_price_ranges(cat)
    cost = np.random.randint(low, high)

    if cat == "Groceries":
        price = cost * np.random.uniform(1.08, 1.35)
    elif cat == "Clothing":
        price = cost * np.random.uniform(1.15, 1.60)
    elif cat == "Electronics":
        price = cost * np.random.uniform(1.20, 1.90)
    else:
        price = cost * np.random.uniform(1.18, 1.75)

    cost_prices.append(round(cost, 2))
    selling_prices.append(round(price, 2))

products["sub_category"] = subcats
products["cost_price"] = cost_prices
products["selling_price"] = selling_prices

# =====================================================
# ORDERS + ORDER ITEMS
# =====================================================
regions = ["North", "South", "East", "West"]

order_rows = []
order_item_rows = []

for order_id in range(1, NUM_ORDERS + 1):
    order_date = generate_order_date()
    month = order_date.month

    customer_id = np.random.randint(1, NUM_CUSTOMERS + 1)
    customer_segment = customers.loc[customers["customer_id"] == customer_id, "segment"].iloc[0]

    region = weighted_choice(regions, [0.26, 0.29, 0.23, 0.22])

    payment_probs = segment_preferences(customer_segment)
    payment_method = weighted_choice(
        ["Cash", "Card", "Online"],
        [payment_probs["cash"], payment_probs["card"], payment_probs["online"]]
    )

    order_rows.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "region": region,
        "store_id": np.random.randint(1, 50),
        "payment_method": payment_method
    })

    # Choose category using region preference + seasonal influence
    pref = region_preferences(region)

    # Seasonality influence by category
    if month == 11:
        pref["Electronics"] += 0.15
        pref["Clothing"] += 0.10
    if month == 12:
        pref["Clothing"] += 0.15
        pref["Electronics"] += 0.10
    if month in [1, 2]:
        pref["Groceries"] += 0.08

    category = weighted_choice(
        list(pref.keys()),
        list(pref.values())
    )

    # Choose product from category
    cat_products = products[products["category"] == category]
    chosen_product = cat_products.sample(1, random_state=random.randint(1, 999999)).iloc[0]

    discount = generate_discount(month, category, customer_segment)
    quantity = generate_quantity(category, customer_segment, month, discount)

    # Make order line item
    order_item_rows.append({
        "order_item_id": order_id,
        "order_id": order_id,
        "product_id": int(chosen_product["product_id"]),
        "quantity": quantity,
        "discount": discount
    })

orders = pd.DataFrame(order_rows)
order_items = pd.DataFrame(order_item_rows)

# =====================================================
# SAVE FILES
# =====================================================
customers.to_csv("data/raw/customers.csv", index=False)
products.to_csv("data/raw/products.csv", index=False)
orders.to_csv("data/raw/orders.csv", index=False)
order_items.to_csv("data/raw/order_items.csv", index=False)

print("Advanced retail dataset generated successfully!")
print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
print(f"Order Items: {len(order_items)}")