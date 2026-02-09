import pandas as pd
from logic.excel_reader import detect_order_id_column


def find_column(df, keywords):
    for col in df.columns:
        col_low = col.lower().replace("_", "").replace("-", "")
        for kw in keywords:
            if kw in col_low:
                return col
    return None


def generate_order_profit(order_df, payment_df):
    order_df = order_df.copy()
    payment_df = payment_df.copy()

    # ---------- ORDER ID DETECTION ----------
    order_col_order = detect_order_id_column(order_df)
    order_col_payment = detect_order_id_column(payment_df)

    # ---------- SKU / PRODUCT / ASIN ----------
    sku_col = find_column(order_df, ["sku"])
    name_col = find_column(order_df, ["product", "title", "item", "name"])
    asin_col = find_column(order_df, ["asin"])

    # ---------- CLEAN AMOUNT ----------
    payment_df["amount"] = pd.to_numeric(
        payment_df["Total (INR)"], errors="coerce"
    ).fillna(0)

    rows = []

    # ⚠️ ONLY ORDERS WHICH EXIST IN PAYMENT SHEET
    for order_id in payment_df[order_col_payment].dropna().unique():
        sub = payment_df[payment_df[order_col_payment] == order_id]

        income = sub[sub["amount"] > 0]["amount"].sum()
        expense = abs(sub[sub["amount"] < 0]["amount"].sum())
        profit = income - expense

        order_row = order_df[order_df[order_col_order] == order_id]

        sku = (
            order_row[sku_col].iloc[0]
            if sku_col and not order_row.empty
            else ""
        )

        product_name = (
            order_row[name_col].iloc[0]
            if name_col and not order_row.empty
            else ""
        )

        asin = (
            order_row[asin_col].iloc[0]
            if asin_col and not order_row.empty
            else ""
        )

        rows.append({
            "Order ID": order_id,
            "SKU": sku,
            "Product Name": product_name,
            "ASIN": asin,
            "Income": round(income, 2),
            "Expense": round(expense, 2),
            "Profit": round(profit, 2),
            "Status": "PROFIT" if profit > 0 else "LOSS"
        })

    # ---------- FINAL ORDER ----------
    return pd.DataFrame(rows)[[
        "Order ID",
        "SKU",
        "Product Name",
        "ASIN",
        "Income",
        "Expense",
        "Profit",
        "Status"
    ]]
