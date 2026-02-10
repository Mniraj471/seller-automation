import pandas as pd

# ================= UNIVERSAL MULTI SHEET READER =================
def read_excel_safely(file_path, mode="payment"):
    """
    mode = payment | order
    """
    xls = pd.ExcelFile(file_path, engine="openpyxl")

    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sheet)

            if df.empty:
                continue

            cols = [c.lower() for c in df.columns.astype(str)]

            # ---------- PAYMENT SHEET DETECTION ----------
            if mode == "payment":
                payment_signatures = [
                    "total (inr)",                  # Amazon
                    "final settlement amount",      # Meesho
                    "bank settlement value",        # Flipkart
                    "invoice amount",               # Snapdeal
                ]

                if any(sig in c for sig in payment_signatures for c in cols):
                    print(f"✅ PAYMENT SHEET DETECTED → {sheet}")
                    return df

            # ---------- ORDER SHEET DETECTION ----------
            if mode == "order":
                order_signatures = [
                    "order id",
                    "sub order",
                    "order_item_id",
                    "suborder id",
                ]

                if any(sig in c for sig in order_signatures for c in cols):
                    print(f"✅ ORDER SHEET DETECTED → {sheet}")
                    return df

        except Exception:
            continue

    raise Exception("❌ No valid sheet found in Excel file")
