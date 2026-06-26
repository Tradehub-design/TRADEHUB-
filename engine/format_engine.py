class FormatEngine:

    @staticmethod
    def currency(value):

        try:
            return f"${float(value):,.2f}"
        except Exception:
            return "$0.00"

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
