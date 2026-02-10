import pandas as pd

# ================= SAFE EXCEL READER =================
def read_excel_safely(file_path, mode="payment"):
    """
    Reads ALL sheets from Excel and merges them safely.
    Ignores empty / formula-only / note sheets.
    """

    try:
        xls = pd.ExcelFile(file_path, engine="openpyxl")
    except Exception as e:
        raise Exception(f"Excel read error: {e}")

    all_dfs = []

    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet)
        except Exception:
            continue

        if df is None or df.empty:
            continue

        # Drop fully empty rows/cols
        df = df.dropna(how="all").dropna(axis=1, how="all")

        if len(df.columns) < 3:
            continue

        all_dfs.append(df)

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, ignore_index=True)


# ================= ORDER ID DETECTOR =================
def detect_order_id_column(df):
    """
    Detects Order ID / Sub Order ID column automatically
    for Amazon / Flipkart / Meesho / Snapdeal
    """

    possible_columns = [
        "order id",
        "amazon-order-id",
        "order_item_id",
        "order_item_id",
        "sub order no",
        "suborder id",
        "sub order id",
        "order_item_id",
        "order id",
        "suborder id",
        "order_item_id",
        "order_item_id",
        "order_item_id",
    ]

    for col in df.columns:
        col_lower = col.lower().strip()
        for key in possible_columns:
            if key in col_lower:
                return col

    raise Exception("❌ Order ID column not found in order sheet")
