class FormatEngine:

    @staticmethod
    def currency(value, symbol="$"):
        try:
            return f"{symbol}{float(value):,.2f}"
        except Exception:
            return f"{symbol}0.00"

    @staticmethod
    def signed_currency(value, symbol="$"):
        try:
            number = float(value)
            sign = "+" if number > 0 else ""
            return f"{sign}{symbol}{number:,.2f}"
        except Exception:
            return f"{symbol}0.00"

    @staticmethod
    def percent(value):
        try:
            return f"{float(value):.2f}%"
        except Exception:
            return "0.00%"

    @staticmethod
    def number(value):
        try:
            return f"{float(value):,.2f}"
        except Exception:
            return "0.00"

    @staticmethod
    def integer(value):
        try:
            return str(int(value))
        except Exception:
            return "0"

    @staticmethod
    def result_status(value):
        try:
            number = float(value)
            if number > 0:
                return "positive"
            if number < 0:
                return "negative"
            return "neutral"
        except Exception:
            return "neutral"
