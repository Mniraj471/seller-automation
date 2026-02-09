import pandas as pd
from logic.excel_reader import detect_order_id_column


def generate_order_mismatch(order_df, payment_df):

    order_df = order_df.copy()
    payment_df = payment_df.copy()

    order_col = detect_order_id_column(order_df)
    payment_col = detect_order_id_column(payment_df)

    order_ids = set(order_df[order_col].dropna().astype(str))
    payment_ids = set(payment_df[payment_col].dropna().astype(str))

    rows = []

    for oid in order_ids:
        if oid in payment_ids:
            status = "PAID"
        else:
            status = "UNPAID"

        rows.append({
            "Order ID": oid,
            "Status": status
        })

    for oid in payment_ids - order_ids:
        rows.append({
            "Order ID": oid,
            "Status": "PAID (ORDER NOT FOUND)"
        })

    return pd.DataFrame(rows)
