import pandas as pd

def calculate_settlement(df, platform, from_date=None, to_date=None):
    platform = platform.lower()
    df = df.copy()

    # ================= AMAZON =================
    if platform == "amazon":
        amount_col = "Total (INR)"
        date_col = "Date"

        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

        income = df[df[amount_col] > 0][amount_col].sum()
        expense = abs(df[df[amount_col] < 0][amount_col].sum())

        return {
            "income": {"order_payment": round(income, 2)},
            "expenses": {"amazon_fee": round(expense, 2)},
            "total_income": round(income, 2),
            "total_expense": round(expense, 2),
            "net_settlement": round(income - expense, 2),
        }

    # ================= MEESHO (🔥 IMPORTANT) =================
    elif platform == "meesho":
        date_col = "Transaction Date"
        net_col = "Final Settlement (B + C + G + AA)"

        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            if from_date:
                df = df[df[date_col] >= pd.to_datetime(from_date)]
            if to_date:
                df = df[df[date_col] <= pd.to_datetime(to_date)]

        df[net_col] = pd.to_numeric(df[net_col], errors="coerce").fillna(0)

        net = df[net_col].sum()

        return {
            "income": {"meesho_net_settlement": round(net, 2)},
            "expenses": {},
            "total_income": round(net, 2),
            "total_expense": 0,
            "net_settlement": round(net, 2),
        }

    # ================= FLIPKART / SNAPDEAL =================
    else:
        raise Exception("Platform not supported yet")
