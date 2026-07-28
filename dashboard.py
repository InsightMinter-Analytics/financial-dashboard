import copy

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_generator import generate_financial_data

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("📊 Interactive Financial Dashboard")


def fmt_inr(value):
    """Format a number as an Indian-style currency string, e.g. ₹15,83,920."""
    value = int(round(value))
    sign = "-" if value < 0 else ""
    value = abs(value)
    s = str(value)
    if len(s) <= 3:
        formatted = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        parts = []
        while len(rest) > 2:
            parts.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            parts.insert(0, rest)
        formatted = ",".join(parts) + "," + last3
    return f"{sign}₹{formatted}"


# --- Data generation (seeded so it doesn't reshuffle on every interaction) ---
st.sidebar.header("Data Controls")
if "seed" not in st.session_state:
    st.session_state.seed = 42

if st.sidebar.button("🔄 Regenerate Data"):
    st.session_state.seed = np.random.default_rng().integers(0, 1_000_000)

base_data = generate_financial_data(seed=st.session_state.seed)

# --- Scenario Switch (button-based toggle) ---
if "scenario" not in st.session_state:
    st.session_state.scenario = "Base Case"

st.write("**Choose Scenario:**")
scenario_options = ["Base Case", "Optimistic", "Pessimistic"]
scenario_icons = {"Base Case": "⚖️", "Optimistic": "📈", "Pessimistic": "📉"}
scenario_cols = st.columns(len(scenario_options))
for col, option in zip(scenario_cols, scenario_options):
    is_active = st.session_state.scenario == option
    if col.button(
        f"{scenario_icons[option]} {option}",
        key=f"scenario_btn_{option}",
        type="primary" if is_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.scenario = option

scenario = st.session_state.scenario

# Work on a copy so the cached base data is never mutated.
data = copy.deepcopy(base_data)

if scenario == "Optimistic":
    data["revenue"] *= 1.2
    for k in data["expenses"]:
        data["expenses"][k] *= 0.9
elif scenario == "Pessimistic":
    data["revenue"] *= 0.8
    for k in data["expenses"]:
        data["expenses"][k] *= 1.1

total_expenses = sum(data["expenses"].values())

# Recompute cash flow proportionally so scenario changes flow through consistently.
if base_data["revenue"] > 0:
    scale = data["revenue"] / base_data["revenue"]
else:
    scale = 1.0
data["cash_flow"] = data["revenue"] - total_expenses

# --- KPI Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Revenue", fmt_inr(data["revenue"]))
col2.metric("Expenses", fmt_inr(total_expenses))
col3.metric("Cash Flow", fmt_inr(data["cash_flow"]))

col4, col5, col6 = st.columns(3)
col4.metric("Receivables", fmt_inr(data["receivables"]))
col5.metric("Payables", fmt_inr(data["payables"]))
col6.metric("GST Liability", fmt_inr(data["gst_liability"]))

# --- Financial Health Indicator (bounded 0-100) ---
profit = data["revenue"] - total_expenses
profit_margin = profit / data["revenue"] if data["revenue"] > 0 else 0
profit_margin_score = max(0.0, min(profit_margin, 1.0)) * 50  # 0-50

cash_flow_score = 20 if data["cash_flow"] > 0 else 0  # 0 or 20

payables_safe = data["payables"] + 1
receivable_ratio = data["receivables"] / payables_safe
# Reward receivables covering payables, but cap contribution so an
# extreme ratio can't push the score past its 30-point share.
liquidity_score = min(receivable_ratio, 1.0) * 30  # 0-30

health_score = profit_margin_score + cash_flow_score + liquidity_score

st.subheader("💡 Financial Health")
if health_score > 80:
    st.success(f"🟢 Financial Health: Excellent ({health_score:.0f}/100)")
elif health_score > 50:
    st.warning(f"🟡 Financial Health: Stable ({health_score:.0f}/100)")
else:
    st.error(f"🔴 Financial Health: Weak ({health_score:.0f}/100)")

# --- Scenario Outcome Summary Card ---
st.subheader("📌 Scenario Outcome Summary")
if scenario == "Base Case":
    st.info(
        "The firm is operating under normal conditions. Revenue and expenses "
        "are balanced, and financial health reflects the current market situation."
    )
elif scenario == "Optimistic":
    st.success(
        "Revenue growth and reduced expenses improve profitability. The firm "
        "shows strong financial health, suggesting room for expansion or investment."
    )
elif scenario == "Pessimistic":
    st.error(
        "Revenue decline and rising expenses weaken profitability. The firm "
        "may face cash flow challenges and should consider cost control or risk mitigation."
    )

# --- Regional Sales Breakdown ---
st.subheader("🗺️ Regional Sales Breakdown")
region_df = pd.DataFrame({
    "Region": list(data["region_sales"].keys()),
    "Sales": [v * scale for v in data["region_sales"].values()],
})

# Line chart dropped here: region_sales is a categorical snapshot, not a
# sequence, so a line chart implies a trend that isn't there. Bar and Pie
# are the two chart types that correctly represent this data.
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Bar"

st.write("**Choose Chart Type:**")
chart_options = ["Bar", "Pie"]
chart_cols = st.columns(len(chart_options))
for col, option in zip(chart_cols, chart_options):
    is_active = st.session_state.chart_type == option
    if col.button(
        f"📊 {option}" if option == "Bar" else f"🥧 {option}",
        key=f"chart_btn_{option}",
        type="primary" if is_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.chart_type = option

chart_type = st.session_state.chart_type

if chart_type == "Bar":
    fig = px.bar(region_df, x="Region", y="Sales", title="Regional Sales", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)
elif chart_type == "Pie":
    fig = px.pie(region_df, names="Region", values="Sales", title="Regional Sales")
    st.plotly_chart(fig, use_container_width=True)

# --- Forecasting Example ---
st.subheader("📈 Revenue Forecast")

historical_revenue = data["historical_revenue"]
forecast = float(np.mean(historical_revenue[-3:]))  # simple 3-month moving average

months = [f"Month {i+1}" for i in range(len(historical_revenue))] + ["Forecast"]
values = historical_revenue + [forecast]

fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(
    x=months[:-1], y=values[:-1], mode="lines+markers", name="Actual Revenue"
))
fig_forecast.add_trace(go.Scatter(
    x=months[-2:], y=values[-2:], mode="lines+markers", name="Forecast",
    line=dict(dash="dash"),
))
fig_forecast.update_layout(
    xaxis_title="Period", yaxis_title="Revenue (₹)", legend_title_text=""
)
st.plotly_chart(fig_forecast, use_container_width=True)

st.caption(
    f"Forecast is a simple 3-month moving average of the last 3 months: {fmt_inr(forecast)}"
)
