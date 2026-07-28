import numpy as np


def generate_financial_data(seed=None):
    """Generate a synthetic snapshot of financial data for the dashboard.

    Args:
        seed: optional int. Pass the same seed to get the same numbers back
            (used so the dashboard doesn't reshuffle on every widget click).

    Returns:
        dict with revenue, expenses (dict), cash_flow, receivables,
        payables, gst_liability, region_sales (dict), and a 12-month
        historical_revenue list used for forecasting.
    """
    rng = np.random.default_rng(seed)

    revenue = int(rng.integers(800_000, 2_000_000))

    expenses = {
        "Salaries": int(revenue * rng.uniform(0.25, 0.35)),
        "Rent": int(revenue * rng.uniform(0.05, 0.08)),
        "Utilities": int(revenue * rng.uniform(0.02, 0.04)),
        "Marketing": int(revenue * rng.uniform(0.05, 0.10)),
        "Other": int(revenue * rng.uniform(0.03, 0.06)),
    }
    total_expenses = sum(expenses.values())

    cash_flow = revenue - total_expenses - int(revenue * rng.uniform(0.0, 0.05))
    receivables = int(revenue * rng.uniform(0.10, 0.25))
    payables = int(total_expenses * rng.uniform(0.10, 0.20))

    # Illustrative GST liability at ~18% slab on revenue, with some variance.
    gst_liability = int(revenue * 0.18 * rng.uniform(0.8, 1.0))

    region_sales = {
        "North": int(revenue * rng.uniform(0.20, 0.30)),
        "South": int(revenue * rng.uniform(0.20, 0.30)),
        "East": int(revenue * rng.uniform(0.15, 0.25)),
        "West": int(revenue * rng.uniform(0.15, 0.25)),
    }

    historical_revenue = [int(rng.integers(80_000, 200_000)) for _ in range(12)]

    return {
        "revenue": revenue,
        "expenses": expenses,
        "cash_flow": cash_flow,
        "receivables": receivables,
        "payables": payables,
        "gst_liability": gst_liability,
        "region_sales": region_sales,
        "historical_revenue": historical_revenue,
    }
