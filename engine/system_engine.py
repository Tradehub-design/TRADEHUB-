from datetime import datetime


class SystemEngine:

    @staticmethod
    def now():

        return datetime.now()

    @staticmethod
    def today():

        return datetime.now().date()

    @staticmethod
    def timestamp():

        return datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
