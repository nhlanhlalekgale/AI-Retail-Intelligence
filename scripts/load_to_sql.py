import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect("retail.db")

# Load CSV files
customers = pd.read_csv("data/raw/customers.csv")
products = pd.read_csv("data/raw/products.csv")
orders = pd.read_csv("data/raw/orders.csv")
order_items = pd.read_csv("data/raw/order_items.csv")

# Insert data into tables
customers.to_sql("customers", conn, if_exists="append", index=False)
products.to_sql("products", conn, if_exists="append", index=False)
orders.to_sql("orders", conn, if_exists="append", index=False)
order_items.to_sql("order_items", conn, if_exists="append", index=False)

print("Data loaded successfully!")

conn.close()