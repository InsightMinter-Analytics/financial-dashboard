import random
import pandas as pd

def generate_financial_data():
    return {
        "timestamp": pd.Timestamp.now(),
        "revenue": random.randint(50000, 150000),
        "expenses": random.randint(20000, 80000),
        "cash_flow": random.randint(-10000, 50000),
        "receivables": random.randint(10000, 40000),
        "payables": random.randint(5000, 30000),
        "inventory_value": random.randint(20000, 100000),
        "gst_liability": random.randint(2000, 15000)
    }
