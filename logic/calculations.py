import pandas as pd


# ================= PLATFORM COLUMN MAP =================
PLATFORM_MAP = {
    "amazon": {
        "amount": "Total (INR)",
        "desc": "Transaction type",
        "date": "Posted Date"
    },
    "flipkart": {
        "amount": "Amount",
        "desc": "Type",
        "date": "Order Date"
    },
    "meesho": {
        "amount": "Net Amount",
        "desc": "Transaction Type",
        "date": "Settlement Date"
    },
    "snapdeal": {
        "amount": "Amount",
        "desc": "Description",
        "date": "Date"
    }
}


# ================= DATE FILTER =================
def filter_by_date(df, date_col, from_date=None, to_date=None):
    if date_col not in df.columns:
        return df

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    if from_date:
        df = df[df[date_col] >= pd.to_datetime(from_date)]

    if to_date:
        df = df[df[date_col] <= pd.to_datetime(to_date)]

    return df


# ================= MAIN SETTLEMENT LOGIC =================
def calculate_settlement(df, platform, from_date=None, to_date=None):
    platform = platform.lower()

    if platform not in PLATFORM_MAP:
        raise Exception(f"Unsupported platform: {platform}")

    cfg = PLATFORM_MAP[platform]
    amount_col = cfg["amount"]
    desc_col = cfg["desc"]
    date_col = cfg["date"]

    df = df.copy()

    # 🔹 DATE FILTER
    df = filter_by_date(df, date_col, from_date, to_date)

    # 🔹 CLEAN AMOUNT
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

    # 🔹 DESCRIPTION MERGE (SAFE)
    df["desc"] = df[desc_col].astype(str).str.lower()

    if "Product Details" in df.columns:
        df["desc"] += " " + df["Product Details"].astype(str).str.lower()

    # ================= BUCKETS =================
    expenses = {
        "advertising": 0.0,
        "commission": 0.0,
        "shipping": 0.0,
        "refund": 0.0,
        "service_fee": 0.0,
        "subscription": 0.0,
        "other_expense": 0.0,
    }

    income = {
        "order_payment": 0.0,
        "reimbursement": 0.0,
    }

    # ================= CLASSIFICATION =================
    for _, row in df.iterrows():
        amt = row[amount_col]
        desc = row["desc"]

        # 🟢 INCOME
        if amt > 0:
            if any(x in desc for x in ["reimbursement", "lost", "damaged", "reversal"]):
                income["reimbursement"] += amt
            else:
                income["order_payment"] += amt

        # 🔴 EXPENSE
        else:
            val = abs(amt)

            if "refund" in desc:
                expenses["refund"] += val
            elif "commission" in desc:
                expenses["commission"] += val
            elif any(x in desc for x in ["shipping", "easy ship", "delivery"]):
                expenses["shipping"] += val
            elif "advertising" in desc or "ads" in desc:
                expenses["advertising"] += val
            elif "subscription" in desc:
                expenses["subscription"] += val
            elif "service" in desc or "fee" in desc:
                expenses["service_fee"] += val
            else:
                expenses["other_expense"] += val

    # ================= CLEAN OUTPUT =================
    def clean_dict(d):
        return {k: round(v, 2) for k, v in d.items() if round(v, 2) != 0}

    income = clean_dict(income)
    expenses = clean_dict(expenses)

    total_income = round(sum(income.values()), 2)
    total_expense = round(sum(expenses.values()), 2)

    net_settlement = round(total_income - total_expense, 2)

    return {
        "income": income,
        "expenses": expenses,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_settlement": net_settlement,
    }
