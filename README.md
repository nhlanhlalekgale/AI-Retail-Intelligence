# 📊 AI Retail Intelligence Dashboard

## End-to-End Retail Analytics, Machine Learning Forecasting & Business Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SQL](https://img.shields.io/badge/SQL-SQLite-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Revenue%20Forecasting-green)
![Power BI](https://img.shields.io/badge/Power%20BI-Analytics-yellow)

---

# Project Overview

The **AI Retail Intelligence Dashboard** is an end-to-end analytics platform designed to transform raw retail transaction data into actionable business insights.

The project simulates a real-world retail environment where business leaders need to understand:

- Sales performance
- Customer behaviour
- Product performance
- Regional opportunities
- Seasonal demand
- Revenue forecasting
- Business strategy recommendations

The solution combines:

- Synthetic data generation
- SQL database management
- Python analytics
- Machine learning forecasting
- Interactive Streamlit dashboard
- AI-powered business recommendations

---

# Business Problem

Retail organisations generate large amounts of transaction data but often struggle to convert data into strategic decisions.

Key business questions:

### Sales

- Which products generate the highest revenue?
- Which regions perform best?
- How does revenue change over time?

### Customers

- Which customer segments generate the most value?
- How can customer retention improve?

### Operations

- How should inventory be planned?
- When should promotions run?

### Strategy

- What impact will discounts and campaigns have?
- What revenue can be expected in future scenarios?

---

# Solution Architecture


```
Synthetic Data Generator

        ↓

SQLite Retail Database

        ↓

Python Data Analysis

        ↓

Machine Learning Revenue Forecast Model

        ↓

AI Revenue Forecast Simulator

        ↓

Streamlit Business Intelligence Dashboard

        ↓

GitHub Portfolio Deployment
```

---

# Technology Stack

## Programming

- Python
- Pandas
- NumPy

## Database

- SQLite
- SQL Queries
- Relational Data Modelling

## Analytics

- Exploratory Data Analysis
- Feature Engineering
- Revenue Analysis
- Customer Segmentation

## Visualization

- Plotly
- Streamlit
- Power BI

## Machine Learning

- Scikit-Learn
- Regression Forecasting
- Model Evaluation
- Scenario Simulation

## Development Tools

- VS Code
- Git
- GitHub
- Conda Environment

---

# Dataset Design

The retail database contains:

## Orders Table

Stores transaction information:

- Order ID
- Order Date
- Region
- Payment Method
- Customer ID


## Customers Table

Customer attributes:

- Customer ID
- Gender
- Age
- City
- Customer Segment


## Products Table

Product information:

- Product ID
- Product Name
- Category
- Sub-category
- Cost Price
- Selling Price


## Order Items Table

Transaction details:

- Quantity
- Discount


---

# Data Pipeline

## 1. Synthetic Data Generation

Created realistic retail data including:

- Seasonal purchasing patterns
- Black Friday spikes
- Holiday demand
- Customer segments
- Regional behaviour
- Discount sensitivity


---

## 2. SQL Database Development

Built a relational SQLite database:

```
orders

customers

products

order_items
```

Created SQL joins to combine transaction, customer and product information.

---

## 3. Python Analytics Pipeline

Performed:

- Data cleaning
- Feature engineering
- Revenue calculation
- Profit calculation
- Customer analysis
- Product analysis

Revenue formula:

```
Revenue =
Selling Price × Quantity × (1 - Discount)
```


Profit formula:

```
Profit =
(Selling Price - Cost Price)
× Quantity
× (1 - Discount)
```

---

# Dashboard Features

# 1. Executive Summary Dashboard

Provides high-level business KPIs:

- Total Revenue
- Total Profit
- Total Orders
- Total Quantity
- Average Order Value

Purpose:

Allows executives to quickly understand business performance.

---

# 2. Sales Performance Analytics

Includes:

## Monthly Revenue Trends

Tracks sales growth and seasonal movement.

## Revenue By Region

Identifies strongest and weakest markets.

## Revenue By Category

Highlights product categories driving revenue.

## Payment Analysis

Shows customer payment preferences.

## Top Products

Identifies highest revenue-generating products.

---

# 3. Customer Analytics

Analyses customer behaviour:

- Premium customers
- Regular customers
- Customer segments
- Revenue contribution

Provides strategies for:

- Retention
- Loyalty programs
- Customer lifetime value growth

---

# 4. AI Revenue Forecast Simulator

Interactive business simulation tool.

Users can adjust:

- Region
- Product Category
- Customer Segment
- Discount Percentage
- Marketing Spend
- Season
- Campaign Type


The simulator provides:

- Predicted Revenue
- Expected Growth %
- Business Recommendation


Example:

A manager can test:

> "What happens if Black Friday marketing investment increases while offering a 10% discount?"

The system estimates the potential revenue impact.

---

# Machine Learning Forecasting

The forecasting pipeline supports:

- Revenue prediction
- Business scenario modelling
- Demand planning


Model evaluation:

```
MAE:
R152,039.98


RMSE:
R249,380.12


R² Score:
0.9853
```

---

# Retail Analytics Business Insights & Recommendations


# 1. Seasonal Revenue Trends

## Insight

Analysis shows strong seasonal purchasing patterns, with Black Friday and holiday periods generating approximately **80% higher revenue** compared to normal trading periods.

Revenue spikes indicate customers are highly responsive to:

- Promotional campaigns
- Discounts
- Seasonal offers


## Recommendations


### Create Seasonal Marketing Campaigns

Actions:

- Launch Black Friday campaigns 4-6 weeks earlier.
- Use email marketing, social media advertising and targeted promotions.
- Create urgency through limited-time offers.


Expected Impact:

- Increased customer traffic.
- Higher conversion rates.
- Better competitive positioning.


---

### Improve Inventory Planning

Actions:

- Increase inventory before November and December.
- Reduce excess inventory after peak periods.
- Use AI forecasting for demand prediction.


Expected Impact:

- Reduced stock shortages.
- Lower excess inventory.
- Improved customer satisfaction.


---

# 2. Customer Segmentation Strategy


## Insight

Premium customers generate higher revenue compared to Regular and Wholesale customers.

Premium customers show:

- Stronger purchasing behaviour.
- Higher customer lifetime value.


## Recommendations


## Introduce Loyalty Programs

Actions:

- Purchase points.
- Exclusive discounts.
- Early access promotions.
- VIP membership benefits.


Expected Impact:

- Higher retention.
- Increased repeat purchases.
- Improved customer lifetime value.


---

## Convert Regular Customers Into Premium Customers


Actions:

- Personalized recommendations.
- Spending milestones.
- Membership incentives.


Example:

```
Spend R5,000 and unlock Premium Membership
```


Expected Impact:

- Increased average customer spending.
- Stronger customer relationships.


---

# 3. Product Portfolio Strategy


## Insight

Electronics and Furniture generate the highest revenue contribution.

Lower-performing categories require additional support.


## Recommendations


## Prioritize High Performing Categories

Actions:

- Maintain inventory availability.
- Negotiate supplier pricing.
- Introduce premium ranges.
- Create product bundles.


Examples:

Electronics:

- Laptop + accessories bundle
- Smartphone protection package


Furniture:

- Living room packages
- Bedroom furniture bundles


Expected Impact:

- Higher average order value.
- Improved margins.
- Stronger market position.


---

## Improve Low Performing Categories


Actions:

- Targeted discounts.
- Bundle promotions.
- Pricing optimisation.
- Better product visibility.


Examples:

Clothing:

```
Buy 2 Get 1 Free
```

Groceries:

```
Essential Household Package
```


Expected Impact:

- Faster inventory movement.
- Improved profitability.


---

# 4. Discount Strategy Optimization


## Insight

Discounts increase purchasing behaviour, but excessive discounting can reduce profitability.


## Recommendations


Implement smart discounting:

- Higher discounts for slow-moving products.
- Lower discounts for high-demand products.
- Personalized customer offers.


Expected Impact:

- Higher sales volume.
- Protected profit margins.
- Reduced revenue leakage.


---

# 5. Regional Performance Optimization


## Insight

Regional analysis shows differences in customer demand.

South region performs strongest while weaker regions require additional focus.


## Recommendations


Actions:

- Study regional preferences.
- Increase local campaigns.
- Improve product availability.
- Create regional promotions.


Expected Impact:

- Increased regional revenue.
- Expanded customer base.
- Balanced growth.


---

# 6. Payment Method Strategy


## Insight

Card payments represent the dominant payment method.

Customers prefer convenient digital transactions.


## Recommendations


Actions:

- Improve digital payment availability.
- Integrate loyalty programs with payments.
- Promote cashless transactions.


Expected Impact:

- Faster transactions.
- Better customer experience.
- Improved data tracking.


---

# 7. AI Forecasting Recommendations


## Insight

The AI Revenue Forecast Simulator enables managers to test business scenarios before implementation.


## Recommendations


Use AI forecasting to:

- Test promotions.
- Predict discount impact.
- Estimate future revenue.
- Support inventory decisions.


Example:

```
Increase marketing spend by 20%

↓

Forecast expected revenue growth

↓

Adjust strategy before investment
```


Expected Impact:

- Data-driven decisions.
- Reduced business risk.
- Better strategic planning.


---

# Future Improvements

Future development:

- Real-time API data ingestion
- Cloud deployment
- Advanced time-series forecasting
- Automated reporting
- Generative AI business assistant
- Customer recommendation engine


---

# Project Author

**Nhlanhla Lekgale**

Data Analytics | Business Intelligence | AI Solutions

---

# License

MIT License