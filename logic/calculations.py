import pandas as pd

def calculate_settlement(df, platform, from_date=None, to_date=None):
    platform = platform.lower()
    df = df.copy()

    # ================= AMAZON =================
    if platform == "amazon":
        amount_col = "Total (INR)"
        desc_col = "Transaction type"
        date_col = "Date"

    # ================= MEESHO =================
    elif platform == "meesho":
        amount_col = "Amount"
        desc_col = "Type"
        date_col = "Settlement Date"

    # ================= FLIPKART =================
    elif platform == "flipkart":
        amount_col = "Amount"
        desc_col = "Transaction Type"
        date_col = "Date"

    # ================= SNAPDEAL =================
    elif platform == "snapdeal":
        amount_col = "Amount"
        desc_col = "Description"
        date_col = "Transaction Date"

    else:
        raise Exception("Unsupported platform")

    # ---------- DATE FILTER ----------
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        if from_date:
            df = df[df[date_col] >= pd.to_datetime(from_date)]
        if to_date:
            df = df[df[date_col] <= pd.to_datetime(to_date)]

    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

    income = {}
    expense = {}

    for _, row in df.iterrows():
        amt = row[amount_col]
        desc = str(row.get(desc_col, "")).lower()

        if amt > 0:
            income.setdefault("order_payment", 0)
            income["order_payment"] += amt
        else:
            expense.setdefault("platform_fee", 0)
            expense["platform_fee"] += abs(amt)

    return {
        "income": {k: round(v, 2) for k, v in income.items()},
        "expenses": {k: round(v, 2) for k, v in expense.items()},
        "total_income": round(sum(income.values()), 2),
        "total_expense": round(sum(expense.values()), 2),
        "net_settlement": round(sum(income.values()) - sum(expense.values()), 2),
    }
