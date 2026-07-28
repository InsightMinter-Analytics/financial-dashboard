import streamlit as st
import pandas as pd
from data_generator import generate_financial_data

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Real-Time Financial Dashboard")

# Generate synthetic data
data = generate_financial_data()
df = pd.DataFrame([data])

# KPI Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"₹{data['revenue']}")
col2.metric("Expenses", f"₹{data['expenses']}")
col3.metric("Cash Flow", f"₹{data['cash_flow']}")

col4, col5, col6 = st.columns(3)
col4.metric("Receivables", f"₹{data['receivables']}")
col5.metric("Payables", f"₹{data['payables']}")
col6.metric("GST Liability", f"₹{data['gst_liability']}")

# Charts
st.line_chart(df[["revenue","expenses"]])
st.bar_chart(df[["receivables","payables"]])
