import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# CONNECT DATABASE
conn = sqlite3.connect("retail.db")

# =====================================================
# 1. REVENUE BY CATEGORY
# =====================================================

query1 = """
SELECT
    p.category,
    (p.selling_price * oi.quantity) AS revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
"""

df1 = pd.read_sql(query1, conn)

category_sales = (
    df1.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))

category_sales.plot(kind="bar")

plt.title("Revenue by Category", fontsize=16)
plt.xlabel("Category")
plt.ylabel("Revenue (R)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("outputs/charts/revenue_by_category.png")

plt.show()

# =====================================================
# 2. MONTHLY SALES TREND
# =====================================================

query2 = """
SELECT
    o.order_date,
    (p.selling_price * oi.quantity) AS revenue
FROM order_items oi

JOIN orders o
ON oi.order_id = o.order_id

JOIN products p
ON oi.product_id = p.product_id
"""

df2 = pd.read_sql(query2, conn)

df2["order_date"] = pd.to_datetime(df2["order_date"])

df2["month"] = df2["order_date"].dt.to_period("M")

monthly_sales = (
    df2.groupby("month")["revenue"]
    .sum()
)

plt.figure(figsize=(12,6))

monthly_sales.plot(kind="line")

plt.title("Monthly Revenue Trend", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Revenue (R)")

plt.tight_layout()

plt.savefig("outputs/charts/monthly_sales_trend.png")

plt.show()

# =====================================================
# 3. REVENUE BY REGION
# =====================================================

query3 = """
SELECT
    o.region,
    (p.selling_price * oi.quantity) AS revenue
FROM order_items oi

JOIN orders o
ON oi.order_id = o.order_id

JOIN products p
ON oi.product_id = p.product_id
"""

df3 = pd.read_sql(query3, conn)

region_sales = (
    df3.groupby("region")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))

region_sales.plot(kind="bar")

plt.title("Revenue by Region", fontsize=16)
plt.xlabel("Region")
plt.ylabel("Revenue (R)")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("outputs/charts/revenue_by_region.png")

plt.show()

# =====================================================
# 4. CUSTOMER SEGMENT REVENUE
# =====================================================

query4 = """
SELECT
    c.segment,
    (p.selling_price * oi.quantity) AS revenue
FROM order_items oi

JOIN orders o
ON oi.order_id = o.order_id

JOIN customers c
ON o.customer_id = c.customer_id

JOIN products p
ON oi.product_id = p.product_id
"""

df4 = pd.read_sql(query4, conn)

segment_sales = (
    df4.groupby("segment")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8,8))

segment_sales.plot(kind="pie", autopct='%1.1f%%')

plt.title("Customer Segment Revenue")

plt.ylabel("")

plt.tight_layout()

plt.savefig("outputs/charts/customer_segment_revenue.png")

plt.show()

# =====================================================
# 5. TOP 10 PRODUCTS
# =====================================================

query5 = """
SELECT
    p.product_name,
    (p.selling_price * oi.quantity) AS revenue
FROM order_items oi

JOIN products p
ON oi.product_id = p.product_id
"""

df5 = pd.read_sql(query5, conn)

top_products = (
    df5.groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

top_products.plot(kind="barh")

plt.title("Top 10 Products by Revenue", fontsize=16)
plt.xlabel("Revenue (R)")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("outputs/charts/top_10_products.png")

plt.show()

# =====================================================
# 6. PAYMENT METHOD ANALYSIS
# =====================================================

query6 = """
SELECT
    o.payment_method,
    (p.selling_price * oi.quantity) AS revenue
FROM order_items oi

JOIN orders o
ON oi.order_id = o.order_id

JOIN products p
ON oi.product_id = p.product_id
"""

df6 = pd.read_sql(query6, conn)

payment_sales = (
    df6.groupby("payment_method")["revenue"]
    .sum()
)

plt.figure(figsize=(8,8))

payment_sales.plot(kind="pie", autopct='%1.1f%%')

plt.title("Payment Method Revenue Distribution")

plt.ylabel("")

plt.tight_layout()

plt.savefig("outputs/charts/payment_method_analysis.png")

plt.show()

# CLOSE CONNECTION
conn.close()

print("\nAll visualizations generated successfully!")