def money(value, currency="$"):
    try:
        return f"{currency}{float(value):,.2f}"
    except Exception:
        return f"{currency}0.00"


def percent(value):
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0.00%"


def number(value):
    try:
        return f"{float(value):,.2f}"
    except Exception:
        return "0.00"
