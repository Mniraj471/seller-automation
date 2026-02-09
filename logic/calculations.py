import pandas as pd


# ================= DATE FILTER HELPER =================
def filter_by_date(df, from_date=None, to_date=None):
    if "Posted Date" not in df.columns:
        return df

    df = df.copy()
    df["Posted Date"] = pd.to_datetime(df["Posted Date"], errors="coerce")

    if from_date:
        df = df[df["Posted Date"] >= pd.to_datetime(from_date)]

    if to_date:
        df = df[df["Posted Date"] <= pd.to_datetime(to_date)]

    return df


# ================= MAIN SETTLEMENT LOGIC =================
def calculate_settlement(
    df,
    amount_col="Total (INR)",
    desc_col="Transaction type",
    from_date=None,
    to_date=None
):
    # ---------- SAFETY ----------
    df = df.copy()

    # 🔹 DATE FILTER APPLY (STEP 5.1)
    df = filter_by_date(df, from_date, to_date)

    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

    df["desc"] = (
        df[desc_col].astype(str).str.lower()
        + " "
        + df.get("Product Details", "").astype(str).str.lower()
    )

    # ---------- EXPENSE BUCKETS ----------
    expenses = {
        "advertising": 0.0,
        "commission": 0.0,
        "shipping": 0.0,
        "refund": 0.0,
        "service_fee": 0.0,
        "subscription": 0.0,
        "other_expense": 0.0,
    }

    # ---------- INCOME BUCKETS ----------
    income = {
        "order_payment": 0.0,
        "reimbursement": 0.0,
    }

    # ---------- CLASSIFICATION ----------
    for _, row in df.iterrows():
        amt = row[amount_col]
        desc = row["desc"]

        # 🟢 INCOME (Bank credit)
        if amt > 0:
            if "order payment" in desc:
                income["order_payment"] += amt
            elif "reimbursement" in desc or "lost" in desc or "damaged" in desc:
                income["reimbursement"] += amt
            elif "weight handling fees reversal" in desc:
                income["reimbursement"] += amt
            else:
                income["order_payment"] += amt

        # 🔴 EXPENSE (Amazon deductions)
        else:
            val = abs(amt)

            if "refund" in desc:
                expenses["refund"] += val
            elif "commission" in desc:
                expenses["commission"] += val
            elif "easy ship" in desc or "shipping" in desc:
                expenses["shipping"] += val
            elif "cost of advertising" in desc:
                expenses["advertising"] += val
            elif "subscription" in desc:
                expenses["subscription"] += val
            elif "service fees" in desc:
                expenses["service_fee"] += val
            else:
                expenses["other_expense"] += val

    # ---------- CLEANING ----------
    def clean_dict(d):
        return {k: round(v, 2) for k, v in d.items() if round(v, 2) != 0}

    income = clean_dict(income)
    expenses = clean_dict(expenses)

    total_income = round(sum(income.values()), 2)
    total_expense = round(sum(expenses.values()), 2)

    # ✅ Amazon already gives NET amount
    net_settlement = total_income

    return {
        "income": income,
        "expenses": expenses,
        "total_income": total_income,
        "total_expense": total_expense,
        "net_settlement": net_settlement,
    }
