def classify_negative(amount, description=""):
    """
    Detects reason of negative amount
    """
    desc = description.lower()

    if "commission" in desc:
        return "COMMISSION"
    if "shipping" in desc or "logistics" in desc:
        return "SHIPPING"
    if "rto" in desc:
        return "RTO"
    if "return" in desc or "refund" in desc:
        return "RETURN"
    if "penalty" in desc or "fine" in desc:
        return "PENALTY"

    return "OTHER CHARGE"


def normalize_amount(amount):
    """
    Converts negative to positive for display
    """
    try:
        amt = float(amount)
        return abs(amt)
    except:
        return 0
