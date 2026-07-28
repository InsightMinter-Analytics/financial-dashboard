import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from data_generator import generate_financial_data

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Interactive Financial Dashboard")

# --- Scenario Switch ---
scenario = st.radio("Choose Scenario:", ["Base Case", "Optimistic", "Pessimistic"])

# Generate synthetic data
data = generate_financial_data()

# Apply scenario adjustments
if scenario == "Optimistic":
    data['revenue'] *= 1.2
    for k in data['expenses']:
        data['expenses'][k] *= 0.9
elif scenario == "Pessimistic":
    data['revenue'] *= 0.8
    for k in data['expenses']:
        data['expenses'][k] *= 1.1

# Convert to DataFrame for charts
df = pd.DataFrame([{
    "Revenue": data['revenue'],
    "Expenses": sum(data['expenses'].values()),
    "Cash Flow": data['cash_flow'],
    "Receivables": data['receivables'],
    "Payables": data['payables'],
    "GST Liability": data['gst_liability']
}])

# --- KPI Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"₹{data['revenue']}")
col2.metric("Expenses", f"₹{sum(data['expenses'].values())}")
col3.metric("Cash Flow", f"₹{data['cash_flow']}")

col4, col5, col6 = st.columns(3)
col4.metric("Receivables", f"₹{data['receivables']}")
col5.metric("Payables", f"₹{data['payables']}")
col6.metric("GST Liability", f"₹{data['gst_liability']}")

# --- Financial Health Indicator ---
profit = data['revenue'] - sum(data['expenses'].values())
profit_margin = profit / data['revenue'] if data['revenue'] > 0 else 0
cash_flow_score = 1 if data['cash_flow'] > 0 else 0
receivable_ratio = data['receivables'] / (data['payables']+1)

health_score = (profit_margin*50) + (cash_flow_score*20) + (receivable_ratio*30)

if health_score > 80:
    st.success("🟢 Financial Health: Excellent")
elif health_score > 50:
    st.warning("🟡 Financial Health: Stable")
else:
    st.error("🔴 Financial Health: Weak")

# --- Chart Style Switch ---
chart_type = st.selectbox("Choose Chart Type:", ["Line", "Bar", "Pie"])

region_df = pd.DataFrame({
    "Region": list(data['region_sales'].keys()),
    "Sales": list(data['region_sales'].values())
})

if chart_type == "Line":
    st.line_chart(region_df.set_index("Region"))
elif chart_type == "Bar":
    st.bar_chart(region_df.set_index("Region"))
elif chart_type == "Pie":
    fig = px.pie(region_df, names="Region", values="Sales", title="Regional Sales")
    st.plotly_chart(fig)

# --- Forecasting Example ---
st.subheader("📈 Revenue Forecast")
historical_revenue = [np.random.randint(80000, 200000) for _ in range(12)]
forecast = np.mean(historical_revenue[-3:])  # simple moving average forecast
forecast_series = historical_revenue + [forecast]

st.line_chart(forecast_series)
