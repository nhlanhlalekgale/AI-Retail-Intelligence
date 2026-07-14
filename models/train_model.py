import os
import sqlite3
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =====================================================
# CREATE OUTPUT FOLDERS IF THEY DO NOT EXIST
# =====================================================
os.makedirs("outputs/charts", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)
os.makedirs("models", exist_ok=True)

# =====================================================
# CONNECT DATABASE
# =====================================================
conn = sqlite3.connect("retail.db")

# =====================================================
# LOAD DATA
# =====================================================
query = """
SELECT
    oi.quantity,
    oi.discount,
    p.selling_price,
    p.category,
    p.sub_category,
    o.region,
    o.payment_method,
    c.segment,
    c.gender,
    c.age,
    o.order_date,
    (p.selling_price * oi.quantity * (1 - oi.discount)) AS revenue
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
JOIN orders o
    ON oi.order_id = o.order_id
JOIN customers c
    ON o.customer_id = c.customer_id
"""

df = pd.read_sql(query, conn)

# =====================================================
# BASIC CLEANING
# =====================================================
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"] = df["order_date"].dt.day
df["day_of_week"] = df["order_date"].dt.dayofweek

df = df.drop(columns=["order_date"])

# Drop rows with missing values just in case
df = df.dropna().copy()

# =====================================================
# TARGET
# =====================================================
y = df["revenue"]

# =====================================================
# FEATURES
# =====================================================
X = df.drop(columns=["revenue"])

numeric_features = [
    "quantity",
    "discount",
    "selling_price",
    "age",
    "year",
    "month",
    "day",
    "day_of_week",
]

categorical_features = [
    "category",
    "sub_category",
    "region",
    "payment_method",
    "segment",
    "gender",
]

# =====================================================
# PREPROCESSOR
# =====================================================
preprocessor = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

# =====================================================
# MODEL PIPELINE
# =====================================================
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", model)
])

# =====================================================
# TRAIN TEST SPLIT
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================================
# TRAIN MODEL
# =====================================================
pipeline.fit(X_train, y_train)

# =====================================================
# PREDICTIONS
# =====================================================
predictions = pipeline.predict(X_test)

# =====================================================
# EVALUATION
# =====================================================
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("=" * 50)
print(f"Mean Absolute Error: R{mae:,.2f}")
print(f"Root Mean Squared Error: R{rmse:,.2f}")
print(f"R2 Score: {r2:.4f}")

# =====================================================
# ACTUAL VS PREDICTED DATA
# =====================================================
results = pd.DataFrame({
    "actual_revenue": y_test.values,
    "predicted_revenue": predictions
})

results.to_csv("outputs/reports/model_predictions.csv", index=False)

# =====================================================
# SAVE FEATURE IMPORTANCE
# =====================================================
feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

importances = pipeline.named_steps["model"].feature_importances_

feature_importance = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

feature_importance.to_csv("outputs/reports/feature_importance.csv", index=False)

print("\nTOP 10 IMPORTANT FEATURES")
print("=" * 50)
print(feature_importance.head(10))

# =====================================================
# VISUALIZE ACTUAL VS PREDICTED
# =====================================================
plt.figure(figsize=(10, 6))
plt.scatter(y_test.iloc[:200], predictions[:200])
plt.xlabel("Actual Revenue")
plt.ylabel("Predicted Revenue")
plt.title("Actual vs Predicted Revenue")
plt.tight_layout()
plt.savefig("outputs/charts/actual_vs_predicted.png")
plt.show()

# =====================================================
# FEATURE IMPORTANCE CHART
# =====================================================
top_features = feature_importance.head(10).sort_values(by="importance", ascending=True)

plt.figure(figsize=(12, 6))
plt.barh(top_features["feature"], top_features["importance"])
plt.title("Top 10 Feature Importance")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("outputs/charts/feature_importance.png")
plt.show()

# =====================================================
# SAVE MODEL
# =====================================================
joblib.dump(pipeline, "models/sales_prediction_model.pkl")

print("\nModel saved successfully!")

# =====================================================
# CLOSE CONNECTION
# =====================================================
conn.close()