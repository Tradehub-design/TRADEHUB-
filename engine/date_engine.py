from datetime import datetime


class DateEngine:

    @staticmethod
    def today():

        return datetime.now().date()

    @staticmethod
    def now():

        return datetime.now()

    @staticmethod
    def format(date_value):

        if date_value is None:
            return "-"

        try:
            return date_value.strftime(
                "%d %b %Y"
            )
        except Exception:
            return str(date_value)

    @staticmethod
    def timestamp():

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
