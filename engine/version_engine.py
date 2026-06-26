from core.config import AppConfig


class VersionEngine:

    @staticmethod
    def version():
        return AppConfig.VERSION

    @staticmethod
    def app_name():
        return AppConfig.APP_NAME

    @staticmethod
    def account():
        return AppConfig.DEFAULT_ACCOUNT

    @staticmethod
    def currency():
        return AppConfig.DEFAULT_CURRENCY
