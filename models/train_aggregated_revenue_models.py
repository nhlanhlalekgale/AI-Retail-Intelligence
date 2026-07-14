import sqlite3
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

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

df = pd.read_sql(query, conn)

# =====================================================
# DATE FEATURES
# =====================================================

df["order_date"] = pd.to_datetime(df["order_date"])

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"] = df["order_date"].dt.day
df["day_of_week"] = df["order_date"].dt.dayofweek
df["week_of_year"] = df["order_date"].dt.isocalendar().week.astype(int)

# =====================================================
# SEASONAL FEATURES
# =====================================================

df["is_weekend"] = np.where(
    df["day_of_week"] >= 5,
    1,
    0
)

df["is_payday_period"] = np.where(
    df["day"] >= 25,
    1,
    0
)

df["is_black_friday"] = np.where(
    (df["month"] == 11) &
    (df["day"] >= 20),
    1,
    0
)

df["is_festive_season"] = np.where(
    df["month"] == 12,
    1,
    0
)

# =====================================================
# TARGET VARIABLE
# =====================================================

df["revenue"] = (
    df["selling_price"]
    * df["quantity"]
    * (1 - df["discount"])
)

# =====================================================
# AGGREGATE MONTHLY REVENUE
# =====================================================

monthly = df.groupby([
    "year",
    "month",
    "region",
    "category",
    "segment"
]).agg({
    "revenue": "sum",
    "quantity": "sum",
    "discount": "mean",
    "age": "mean",
    "is_weekend": "mean",
    "is_payday_period": "mean",
    "is_black_friday": "max",
    "is_festive_season": "max"
}).reset_index()

# =====================================================
# TARGET
# =====================================================

y = monthly["revenue"]

# =====================================================
# FEATURES
# =====================================================

X = monthly.drop(columns=["revenue"])

# =====================================================
# ENCODE CATEGORICAL VARIABLES
# =====================================================

X = pd.get_dummies(
    X,
    columns=[
        "region",
        "category",
        "segment"
    ],
    drop_first=True
)

# =====================================================
# TIME-BASED SPLIT
# =====================================================

monthly["date_key"] = (
    monthly["year"].astype(str)
    + "-"
    + monthly["month"].astype(str)
)

dates = sorted(monthly["date_key"].unique())

split_index = int(len(dates) * 0.8)

train_dates = dates[:split_index]
test_dates = dates[split_index:]

train_mask = monthly["date_key"].isin(train_dates)
test_mask = monthly["date_key"].isin(test_dates)

X_train = X[train_mask]
X_test = X[test_mask]

y_train = y[train_mask]
y_test = y[test_mask]

# =====================================================
# MODEL
# =====================================================

model = RandomForestRegressor(
    n_estimators=500,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

# =====================================================
# TRAIN
# =====================================================

model.fit(X_train, y_train)

# =====================================================
# PREDICT
# =====================================================

predictions = model.predict(X_test)

# =====================================================
# EVALUATION
# =====================================================

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("=" * 50)

print(f"MAE: R{mae:,.2f}")
print(f"RMSE: R{rmse:,.2f}")
print(f"R2 Score: {r2:.4f}")

# =====================================================
# FEATURE IMPORTANCE
# =====================================================

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nTOP FEATURES")
print("=" * 50)

print(importance.head(15))

# =====================================================
# SAVE FEATURE IMPORTANCE
# =====================================================

importance.to_csv(
    "outputs/reports/advanced_feature_importance.csv",
    index=False
)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    model,
    "models/advanced_revenue_forecasting_model.pkl"
)

print("\nAdvanced forecasting model saved successfully!")

# =====================================================
# CLOSE
# =====================================================

conn.close()