import pandas as pd

# ================= SAFE EXCEL READER =================
def read_excel_safely(file_path, sheet_name=None):
    try:
        # Agar sheet_name diya ho
        if sheet_name:
            return pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

        # Auto-detect correct sheet
        xls = pd.ExcelFile(file_path, engine="openpyxl")

        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)

            # Skip empty sheets
            if df.empty:
                continue

            # Meesho / Amazon / Flipkart common columns
            important_cols = [
                "Final Settlement",
                "Total (INR)",
                "Transaction type",
                "Order ID",
                "Sub Order No"
            ]

            for col in important_cols:
                if col in df.columns:
                    print(f"✅ Using sheet: {sheet}")
                    return df

        raise Exception("No valid payment sheet found")

    except Exception as e:
        raise Exception(f"Excel read error: {e}")
