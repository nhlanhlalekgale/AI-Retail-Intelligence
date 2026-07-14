import sqlite3
import pandas as pd

# =====================================================
# CONNECT DATABASE
# =====================================================

conn = sqlite3.connect("retail.db")

# =====================================================
# QUERY
# =====================================================

query = """
SELECT

o.order_id,
o.order_date,
o.region,
o.store_id,
o.payment_method,

c.customer_id,
c.name,
c.gender,
c.age,
c.city,
c.segment,

p.product_id,
p.product_name,
p.category,
p.sub_category,
p.cost_price,
p.selling_price,

oi.quantity,
oi.discount

FROM orders o

JOIN customers c
ON o.customer_id = c.customer_id

JOIN order_items oi
ON o.order_id = oi.order_id

JOIN products p
ON oi.product_id = p.product_id
"""

# =====================================================
# LOAD
# =====================================================

df = pd.read_sql(query, conn)

# =====================================================
# REVENUE
# =====================================================

df["revenue"] = (
    df["selling_price"]
    * df["quantity"]
    * (1 - df["discount"])
)

# =====================================================
# PROFIT
# =====================================================

df["profit"] = (
    (df["selling_price"] - df["cost_price"])
    * df["quantity"]
    * (1 - df["discount"])
)

# =====================================================
# DATE FEATURES
# =====================================================

df["order_date"] = pd.to_datetime(df["order_date"])

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%B")
df["quarter"] = df["order_date"].dt.quarter
df["day_of_week"] = df["order_date"].dt.day_name()

# =====================================================
# SAVE
# =====================================================

df.to_csv(
    "outputs/reports/powerbi_retail_dataset.csv",
    index=False
)

print("Power BI dataset exported successfully!")

conn.close()