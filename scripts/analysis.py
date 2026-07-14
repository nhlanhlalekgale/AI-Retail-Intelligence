import pandas as pd
import sqlite3

# Connect to database
conn = sqlite3.connect("retail.db")

# MASTER QUERY
query = """
SELECT
    o.order_id,
    o.order_date,
    o.region,
    o.store_id,
    o.payment_method,
    c.customer_id,
    c.gender,
    c.age,
    c.city,
    c.segment,
    p.product_name,
    p.category,
    p.sub_category,
    p.cost_price,
    p.selling_price,
    oi.quantity,
    oi.discount,

    (p.selling_price * oi.quantity) AS revenue,

    ((p.selling_price - p.cost_price)
    * oi.quantity) AS profit

FROM order_items oi

JOIN orders o
ON oi.order_id = o.order_id

JOIN products p
ON oi.product_id = p.product_id

JOIN customers c
ON o.customer_id = c.customer_id
"""

# Load into dataframe
df = pd.read_sql(query, conn)

# BASIC KPIs
total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()

print("\n========== RETAIL KPI SUMMARY ==========\n")

print(f"Total Revenue: R{total_revenue:,.2f}")
print(f"Total Profit: R{total_profit:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Customers: {total_customers}")

# TOP PRODUCTS
print("\n========== TOP 10 PRODUCTS ==========\n")

top_products = (
    df.groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

# REVENUE BY REGION
print("\n========== REVENUE BY REGION ==========\n")

region_sales = (
    df.groupby("region")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

print(region_sales)

conn.close()