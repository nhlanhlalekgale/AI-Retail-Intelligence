# ==========================================================
# AI RETAIL INTELLIGENCE DASHBOARD
# Streamlit Analytics + ML Revenue Forecasting
# ==========================================================


import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import numpy as np
import joblib
from datetime import datetime



# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(
    page_title="AI Retail Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)



# ==========================================================
# TITLE
# ==========================================================


st.title(
    "📊 AI Retail Intelligence Dashboard"
)

st.markdown(
"""
### Real-Time Retail Analytics & AI Revenue Forecasting

Synthetic Retail Data → SQL Database → Analytics → Machine Learning → Business Intelligence
"""
)



# ==========================================================
# DATABASE CONNECTION
# ==========================================================


@st.cache_data

def load_data():


    conn = sqlite3.connect(
        "retail.db"
    )


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

    ON o.customer_id=c.customer_id


    JOIN order_items oi

    ON o.order_id=oi.order_id


    JOIN products p

    ON oi.product_id=p.product_id


    """



    df=pd.read_sql(
        query,
        conn
    )


    conn.close()


    return df





# Load Data

df=load_data()



# ==========================================================
# FEATURE ENGINEERING
# ==========================================================


df["order_date"]=pd.to_datetime(
    df["order_date"]
)



df["month"]=(
    df["order_date"]
    .dt.strftime("%Y-%m")
)



df["revenue"]=(
    df["selling_price"]
    *
    df["quantity"]
    *
    (1-df["discount"])
)



df["profit"]=(
    (df["selling_price"]-df["cost_price"])
    *
    df["quantity"]
    *
    (1-df["discount"])
)



# ==========================================================
# SIDEBAR FILTERS
# ==========================================================


st.sidebar.header(
    "🔎 Dashboard Filters"
)



region_filter = st.sidebar.multiselect(

    "Region",

    df["region"].unique(),

    default=df["region"].unique()

)



category_filter = st.sidebar.multiselect(

    "Category",

    df["category"].unique(),

    default=df["category"].unique()

)



segment_filter = st.sidebar.multiselect(

    "Customer Segment",

    df["segment"].unique(),

    default=df["segment"].unique()

)




# ==========================================================
# FILTER DATA
# ==========================================================


filtered_df=df[

    (df["region"].isin(region_filter))

    &

    (df["category"].isin(category_filter))

    &

    (df["segment"].isin(segment_filter))

]



st.success(
    f"Loaded {len(filtered_df):,} transactions"
)
# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================


st.markdown("---")

st.header(
    "1. Executive Summary"
)



# KPI Calculations


total_revenue = filtered_df["revenue"].sum()

total_profit = filtered_df["profit"].sum()

total_orders = filtered_df["order_date"].count()

total_quantity = filtered_df["quantity"].sum()

avg_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)



# KPI CARDS


col1,col2,col3,col4 = st.columns(4)



with col1:

    st.metric(
        "💰 Total Revenue",
        f"R {total_revenue:,.2f}"
    )



with col2:

    st.metric(
        "📈 Total Profit",
        f"R {total_profit:,.2f}"
    )



with col3:

    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )



with col4:

    st.metric(
        "📦 Total Quantity",
        f"{total_quantity:,}"
    )



st.metric(
    "Average Order Value",
    f"R {avg_order_value:,.2f}"
)





# ==========================================================
# SALES PERFORMANCE
# ==========================================================


st.markdown("---")

st.header(
    "2. Sales Performance Analytics"
)




# ==========================================================
# MONTHLY REVENUE TREND
# ==========================================================


monthly_sales=(

    filtered_df

    .groupby("month")

    ["revenue"]

    .sum()

    .reset_index()

)



fig_monthly=px.line(

    monthly_sales,

    x="month",

    y="revenue",

    markers=True,

    title="📈 Monthly Revenue Trend"

)



fig_monthly.update_layout(

    xaxis_title="Month",

    yaxis_title="Revenue (R)"

)



st.plotly_chart(

    fig_monthly,

    use_container_width=True

)





# ==========================================================
# REVENUE BY REGION
# ==========================================================


col1,col2=st.columns(2)



region_sales=(

    filtered_df

    .groupby("region")

    ["revenue"]

    .sum()

    .reset_index()

)



fig_region=px.bar(

    region_sales,

    x="region",

    y="revenue",

    title="🌍 Revenue By Region",

    text_auto=True

)



with col1:

    st.plotly_chart(

        fig_region,

        use_container_width=True

    )





# ==========================================================
# REVENUE BY CATEGORY
# ==========================================================



category_sales=(

    filtered_df

    .groupby("category")

    ["revenue"]

    .sum()

    .reset_index()

)



fig_category=px.pie(

    category_sales,

    names="category",

    values="revenue",

    title="🛍 Revenue By Category"

)



with col2:

    st.plotly_chart(

        fig_category,

        use_container_width=True

    )





# ==========================================================
# PAYMENT ANALYSIS
# ==========================================================


payment_sales=(

    filtered_df

    .groupby("payment_method")

    ["revenue"]

    .sum()

    .reset_index()

)



fig_payment=px.pie(

    payment_sales,

    names="payment_method",

    values="revenue",

    hole=0.4,

    title="💳 Payment Method Analysis"

)



st.plotly_chart(

    fig_payment,

    use_container_width=True

)





# ==========================================================
# TOP PRODUCTS
# ==========================================================


st.subheader(
    "🏆 Top Performing Products"
)



top_products=(

    filtered_df

    .groupby("product_name")

    ["revenue"]

    .sum()

    .sort_values(

        ascending=False

    )

    .head(10)

    .reset_index()

)



fig_products=px.bar(

    top_products,

    x="revenue",

    y="product_name",

    orientation="h",

    title="Top 10 Products By Revenue",

    text_auto=True

)



st.plotly_chart(

    fig_products,

    use_container_width=True

)
# ==========================================================
# CUSTOMER ANALYTICS
# ==========================================================


st.markdown("---")

st.header(
    "3. Customer Analytics"
)



# ==========================================================
# CUSTOMER SEGMENT PERFORMANCE
# ==========================================================


segment_sales=(

    filtered_df

    .groupby("segment")

    ["revenue"]

    .sum()

    .reset_index()

)



fig_segment=px.bar(

    segment_sales,

    x="segment",

    y="revenue",

    color="segment",

    title="👥 Revenue By Customer Segment",

    text_auto=True

)



st.plotly_chart(

    fig_segment,

    use_container_width=True

)





# ==========================================================
# PREMIUM VS REGULAR CUSTOMERS
# ==========================================================


premium_revenue=(

    filtered_df[

        filtered_df["segment"]=="Premium"

    ]

    ["revenue"]

    .sum()

)



regular_revenue=(

    filtered_df[

        filtered_df["segment"]=="Regular"

    ]

    ["revenue"]

    .sum()

)



col1,col2=st.columns(2)



with col1:

    st.metric(

        "⭐ Premium Customer Revenue",

        f"R {premium_revenue:,.2f}"

    )



with col2:

    st.metric(

        "👤 Regular Customer Revenue",

        f"R {regular_revenue:,.2f}"

    )





# ==========================================================
# DISCOUNT ELASTICITY ANALYSIS
# ==========================================================


st.markdown("---")

st.subheader(
    "📉 Discount Elasticity Analysis"
)



elasticity=(

    filtered_df

    .groupby("discount")

    ["quantity"]

    .mean()

    .reset_index()

)



fig_discount=px.scatter(

    elasticity,

    x="discount",

    y="quantity",

    size="quantity",

    title="Discount Impact On Quantity Sold"

)



st.plotly_chart(

    fig_discount,

    use_container_width=True

)





# ==========================================================
# CATEGORY SEASONALITY
# ==========================================================


st.markdown("---")

st.subheader(
    "📅 Category Seasonal Trends"
)



seasonality=(

    filtered_df

    .groupby(

        [
            "month",
            "category"
        ]

    )

    ["revenue"]

    .sum()

    .reset_index()

)



fig_seasonality=px.line(

    seasonality,

    x="month",

    y="revenue",

    color="category",

    markers=True,

    title="Revenue Seasonality By Category"

)



st.plotly_chart(

    fig_seasonality,

    use_container_width=True

)





# ==========================================================
# AUTOMATED BUSINESS INSIGHTS
# ==========================================================


st.markdown("---")

st.header(
    "💡 AI Business Recommendations"
)



# Highest category


best_category=(

    category_sales

    .sort_values(

        "revenue",

        ascending=False

    )

    .iloc[0]

)



# Best region


best_region=(

    region_sales

    .sort_values(

        "revenue",

        ascending=False

    )

    .iloc[0]

)



# Best segment


best_segment=(

    segment_sales

    .sort_values(

        "revenue",

        ascending=False

    )

    .iloc[0]

)



recommendations=[]



recommendations.append(

f"""
🏆 **Top Performing Category**

{best_category['category']} generates the highest revenue.

Recommendation:
Increase inventory allocation, maintain stock availability,
and create premium bundles around this category.
"""

)



recommendations.append(

f"""
🌍 **Best Performing Region**

{best_region['region']} is the strongest revenue market.

Recommendation:
Increase marketing investment and replicate successful
strategies in weaker regions.
"""

)



recommendations.append(

f"""
👥 **Customer Strategy**

{best_segment['segment']} customers generate the highest revenue.

Recommendation:
Introduce loyalty rewards, personalized offers,
and retention campaigns.
"""

)



if filtered_df["discount"].mean() > 0.20:


    recommendations.append(

"""
📉 **Discount Strategy**

High discounts are driving purchase volume.

Recommendation:
Use targeted promotions instead of blanket discounts
to protect profit margins.
"""

    )


else:


    recommendations.append(

"""
📈 **Pricing Strategy**

Revenue is being generated without heavy discount dependency.

Recommendation:
Focus on product value, customer experience,
and premium pricing opportunities.
"""

    )




for r in recommendations:

    st.info(r)





# ==========================================================
# DASHBOARD TIMESTAMP
# ==========================================================


st.markdown("---")


st.write(

"🕒 Dashboard Updated:",

datetime.now().strftime(

"%Y-%m-%d %H:%M:%S"

)

)
# ==========================================================
# AI REVENUE FORECAST SIMULATOR
# ==========================================================


st.markdown("---")

st.header(
    "4. 🤖 AI Revenue Forecast Simulator"
)


st.write(
"""
Simulate business scenarios and estimate future revenue performance.

Adjust pricing, campaigns, marketing spend and seasonal factors.
"""
)



# ==========================================================
# LOAD ML MODEL
# ==========================================================


model = None


try:

    model = joblib.load(
        "models/advanced_revenue_forecasting_model.pkl"
    )


    st.success(
        "✅ AI Forecast Model Loaded"
    )


except Exception:


    st.warning(
        "⚠️ ML model not found. Using business simulation engine."
    )





# ==========================================================
# INPUT CONTROLS
# ==========================================================


col1,col2,col3 = st.columns(3)



with col1:


    forecast_region = st.selectbox(

        "🌍 Select Region",

        filtered_df["region"].unique()

    )



with col2:


    forecast_category = st.selectbox(

        "🛍 Select Category",

        filtered_df["category"].unique()

    )



with col3:


    forecast_segment = st.selectbox(

        "👥 Select Customer Segment",

        filtered_df["segment"].unique()

    )





discount_input = st.slider(

    "🏷 Discount Percentage",

    0,

    50,

    10

)



marketing_input = st.slider(

    "📢 Marketing Investment (R)",

    0,

    1000000,

    100000

)



season_input = st.selectbox(

    "📅 Season",

    [

        "Normal",

        "Black Friday",

        "Festive",

        "Summer",

        "Winter"

    ]

)



campaign_input = st.selectbox(

    "🚀 Campaign Type",

    [

        "None",

        "Social Media",

        "Email Marketing",

        "Bundle Promotion",

        "Flash Sale"

    ]

)





# ==========================================================
# FORECAST ENGINE
# ==========================================================


if st.button(
    "🚀 Generate Revenue Forecast"
):


    historical_data = filtered_df[

        (filtered_df["region"]==forecast_region)

        &

        (filtered_df["category"]==forecast_category)

        &

        (filtered_df["segment"]==forecast_segment)

    ]



    if len(historical_data)==0:


        st.error(
            "No historical data available for this combination."
        )


    else:


        base_revenue = historical_data["revenue"].mean()



        # Seasonal impact


        season_factor = {


            "Normal":1.0,

            "Black Friday":1.8,

            "Festive":1.6,

            "Summer":1.15,

            "Winter":1.10

        }



        # Campaign impact


        campaign_factor = {


            "None":1.0,

            "Social Media":1.15,

            "Email Marketing":1.10,

            "Bundle Promotion":1.25,

            "Flash Sale":1.30

        }




        predicted_revenue = (

            base_revenue

            *

            season_factor[season_input]

            *

            campaign_factor[campaign_input]

            *

            (1 + discount_input/100)

            *

            (1 + marketing_input/1000000)

        )



        growth_percentage = (

            (

            predicted_revenue-base_revenue

            )

            /

            base_revenue

        ) * 100





        # ==================================================
        # OUTPUT CARDS
        # ==================================================


        st.success(
            "Forecast Completed"
        )



        col1,col2,col3 = st.columns(3)



        with col1:


            st.metric(

                "Predicted Revenue",

                f"R {predicted_revenue:,.2f}"

            )



        with col2:


            st.metric(

                "Expected Growth",

                f"{growth_percentage:.2f}%"

            )



        with col3:


            st.metric(

                "Current Average Revenue",

                f"R {base_revenue:,.2f}"

            )





        # ==================================================
        # AI RECOMMENDATIONS
        # ==================================================


        st.subheader(
            "🧠 AI Business Recommendation"
        )



        if growth_percentage >= 50:


            recommendation = f"""

🔥 High Growth Opportunity


The selected strategy has strong revenue potential.


Actions:

• Increase inventory before {season_input} demand

• Scale {campaign_input} campaign

• Allocate more marketing budget

• Protect stock availability


"""



        elif growth_percentage >=20:


            recommendation = f"""

📈 Moderate Growth Opportunity


Strategy shows positive potential.


Actions:

• Test campaign on selected segment

• Monitor conversion rate

• Optimise discount level


"""



        else:


            recommendation=f"""

⚠️ Low Growth Scenario


Expected improvement is limited.


Actions:

• Review pricing strategy

• Improve customer targeting

• Reduce unnecessary discounts


"""



        st.info(
            recommendation
        )





# ==========================================================
# DATA PREVIEW
# ==========================================================


st.markdown("---")

st.header(
    "📄 Transaction Data Preview"
)


st.dataframe(

    filtered_df.head(1000),

    use_container_width=True

)





# ==========================================================
# CLOSE
# ==========================================================


st.caption(

f"""
Dashboard generated:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

)