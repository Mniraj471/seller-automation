def match_orders(order_df, payment_df, order_col, payment_col):
    order_df[order_col] = order_df[order_col].astype(str)
    payment_df[payment_col] = payment_df[payment_col].astype(str)

    merged = order_df.merge(
        payment_df,
        left_on=order_col,
        right_on=payment_col,
        how="left",
        indicator=True
    )

    merged["payment_status"] = merged["_merge"].apply(
        lambda x: "PAID" if x == "both" else "PENDING"
    )

    return merged
