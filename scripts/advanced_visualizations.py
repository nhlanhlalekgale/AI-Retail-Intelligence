import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# CONNECT DATABASE
# =====================================================

conn = sqlite3.connect("retail.db")

# =====================================================
# LOAD DATA
# =====================================================

query = """
SELECT

o.order_date,
o.region,
o.payment_method,

c.segment,
c.gender,
c.age,

p.product_name,
p.category,
p.sub_category,
p.selling_price,
p.cost_price,

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


df = pd.read_sql(query, conn)

# =====================================================
# DATE FEATURES
# =====================================================

df["order_date"] = pd.to_datetime(df["order_date"])

df["month"] = df["order_date"].dt.to_period("M")
df["month_name"] = df["order_date"].dt.strftime("%b")
df["year"] = df["order_date"].dt.year

# =====================================================
# REVENUE
# =====================================================

df["revenue"] = (
    df["selling_price"]
    * df["quantity"]
    * (1 - df["discount"])
)

# =====================================================
# STYLE
# =====================================================

plt.style.use("ggplot")

# =====================================================
# 1. MONTHLY SALES TREND
# =====================================================

monthly_sales = df.groupby("month")["revenue"].sum()

plt.figure(figsize=(14,6))

monthly_sales.plot(
    marker="o",
    linewidth=3,
    color="darkblue",
    label="Monthly Revenue"
)

plt.title(
    "Monthly Revenue Trend with Seasonality",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Revenue (Rands)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/charts/monthly_sales_trend.png"
)

plt.show()

# =====================================================
# 2. REVENUE BY REGION
# =====================================================

region_sales = df.groupby("region")["revenue"].sum().sort_values()

plt.figure(figsize=(10,6))

region_sales.plot(
    kind="barh",
    color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
)

plt.title(
    "Revenue by Region",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Revenue (Rands)")
plt.ylabel("Region")

plt.tight_layout()

plt.savefig(
    "outputs/charts/revenue_by_region.png"
)

plt.show()

# =====================================================
# 3. REVENUE BY CATEGORY
# =====================================================

category_sales = df.groupby("category")["revenue"].sum().sort_values()

plt.figure(figsize=(10,6))

category_sales.plot(
    kind="bar",
    color=["purple", "green", "orange", "red"]
)

plt.title(
    "Revenue by Product Category",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Category")
plt.ylabel("Revenue (Rands)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "outputs/charts/revenue_by_category.png"
)

plt.show()

# =====================================================
# 4. CUSTOMER SEGMENT REVENUE
# =====================================================

segment_sales = df.groupby("segment")["revenue"].sum()

plt.figure(figsize=(8,8))

plt.pie(
    segment_sales,
    labels=segment_sales.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=["gold", "skyblue", "lightcoral"]
)

plt.title(
    "Customer Segment Revenue Share",
    fontsize=18,
    fontweight="bold"
)

plt.legend(segment_sales.index)

plt.tight_layout()

plt.savefig(
    "outputs/charts/customer_segment_revenue.png"
)

plt.show()

# =====================================================
# 5. TOP 10 PRODUCTS
# =====================================================

product_sales = (
    df.groupby("product_name")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,7))

product_sales.sort_values().plot(
    kind="barh",
    color="teal"
)

plt.title(
    "Top 10 Revenue Generating Products",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Revenue (Rands)")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_10_products.png"
)

plt.show()

# =====================================================
# 6. PAYMENT METHOD ANALYSIS
# =====================================================

payment_sales = df.groupby("payment_method")["revenue"].sum()

plt.figure(figsize=(8,6))

payment_sales.plot(
    kind="bar",
    color=["#4CAF50", "#2196F3", "#FF9800"]
)

plt.title(
    "Revenue by Payment Method",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Payment Method")
plt.ylabel("Revenue (Rands)")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "outputs/charts/payment_method_analysis.png"
)

plt.show()

# =====================================================
# 7. BLACK FRIDAY & FESTIVE SPIKES
# =====================================================

bf = (
    df.groupby("month")["revenue"]
    .sum()
)

plt.figure(figsize=(14,6))

bf.plot(
    color="crimson",
    linewidth=3,
    marker="o",
    label="Revenue"
)

plt.axvspan(
    21,
    23,
    color="orange",
    alpha=0.3,
    label="Black Friday Period"
)

plt.title(
    "Seasonal Revenue Spikes",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Revenue (Rands)")

plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/charts/seasonal_spikes.png"
)

plt.show()

# =====================================================
# 8. DISCOUNT ELASTICITY
# =====================================================

elasticity = (
    df.groupby("discount")["quantity"]
    .mean()
)

plt.figure(figsize=(10,6))

elasticity.plot(
    marker="o",
    linewidth=3,
    color="darkgreen",
    label="Average Quantity"
)

plt.title(
    "Discount Elasticity vs Quantity Sold",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Discount")
plt.ylabel("Average Quantity")

plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/charts/discount_elasticity.png"
)

plt.show()

# =====================================================
# 9. PREMIUM CUSTOMER BEHAVIOR
# =====================================================

premium = (
    df.groupby("segment")["revenue"]
    .mean()
)

plt.figure(figsize=(10,6))

premium.plot(
    kind="bar",
    color=["#9C27B0", "#03A9F4", "#FF5722"]
)

plt.title(
    "Average Revenue by Customer Segment",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Segment")
plt.ylabel("Average Revenue")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "outputs/charts/premium_customer_behavior.png"
)

plt.show()

# =====================================================
# 10. CATEGORY SEASONALITY
# =====================================================

seasonality = (
    df.groupby(["month", "category"])["revenue"]
    .sum()
    .unstack()
)

plt.figure(figsize=(15,7))

for col in seasonality.columns:
    plt.plot(
        seasonality.index.astype(str),
        seasonality[col],
        linewidth=2,
        marker="o",
        label=col
    )

plt.title(
    "Category Revenue Seasonality",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Month")
plt.ylabel("Revenue (Rands)")

plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/charts/category_seasonality.png"
)

plt.show()

# =====================================================
# CLOSE CONNECTION
# =====================================================

conn.close()

print("\nAdvanced retail visualizations generated successfully!")