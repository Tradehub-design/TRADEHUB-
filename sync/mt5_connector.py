import MetaTrader5 as mt5

from config import (
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER
)


class MT5Connector:

    @staticmethod
    def connect():

        if not mt5.initialize():

            raise Exception(
                f"Unable to initialise MT5: {mt5.last_error()}"
            )

        authorised = mt5.login(
            login=MT5_LOGIN,
            password=MT5_PASSWORD,
            server=MT5_SERVER
        )

        if not authorised:

            raise Exception(
                f"Unable to login: {mt5.last_error()}"
            )

        return True

    @staticmethod
    def disconnect():
        mt5.shutdown()

    @staticmethod
    def account():

        return mt5.account_info()

    @staticmethod
    def positions():

        return mt5.positions_get()

    @staticmethod
    def history(date_from, date_to):

        return mt5.history_deals_get(
            date_from,
            date_to
        )