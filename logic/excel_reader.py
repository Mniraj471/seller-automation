import pandas as pd

def read_excel_safely(file_path):
    try:
        xl = pd.ExcelFile(file_path)
        sheet_name = xl.sheet_names[0]
        df = xl.parse(sheet_name)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        raise Exception(f"Excel read error: {e}")

def detect_order_id_column(df):
    possible_names = [
        "order id", "order-id", "order_id",
        "sub order no", "suborder", "order number",
        "order_no", "sub_order_no"
    ]

    for col in df.columns:
        col_clean = col.lower().replace(" ", "").replace("-", "_")
        for key in possible_names:
            if key.replace(" ", "").replace("-", "_") in col_clean:
                return col

    raise Exception("❌ Order ID column not found")
