import random
import pandas as pd

def generate_financial_data():
    return {
        "timestamp": pd.Timestamp.now(),
        
        # Revenue & Cash Flow
        "revenue": random.randint(80000, 200000),
        "cash_flow": random.randint(-20000, 60000),
        
        # Expense Categories
        "expenses": {
            "salaries": random.randint(30000, 60000),
            "rent": random.randint(10000, 20000),
            "marketing": random.randint(5000, 15000),
            "utilities": random.randint(2000, 8000),
            "misc": random.randint(1000, 5000)
        },
        
        # Regional Sales
        "region_sales": {
            "North": random.randint(20000, 50000),
            "South": random.randint(15000, 40000),
            "East": random.randint(10000, 30000),
            "West": random.randint(15000, 35000)
        },
        
        # Receivables & Payables
        "receivables": random.randint(10000, 40000),
        "payables": random.randint(5000, 30000),
        
        # GST Liability
        "gst_liability": random.randint(2000, 15000),
        
        # Customers & Churn
        "customers": random.randint(500, 2000),
        "churn_rate": round(random.uniform(0.01, 0.05), 2)
    }
