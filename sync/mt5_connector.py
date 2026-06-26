import MetaTrader5 as mt5

from sync.config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
from sync.sync_logger import SyncLogger


class MT5Connector:

    @staticmethod
    def connect():
        if not mt5.initialize():
            raise Exception(f"MT5 initialize failed: {mt5.last_error()}")

        if MT5_LOGIN and MT5_PASSWORD and MT5_SERVER:
            authorised = mt5.login(
                login=int(MT5_LOGIN),
                password=MT5_PASSWORD,
                server=MT5_SERVER,
            )

            if not authorised:
                raise Exception(f"MT5 login failed: {mt5.last_error()}")

        SyncLogger.info("MT5 connected")
        return True

    @staticmethod
    def disconnect():
        mt5.shutdown()
        SyncLogger.info("MT5 disconnected")

    @staticmethod
    def account_info():
        return mt5.account_info()

    @staticmethod
    def open_positions():
        positions = mt5.positions_get()
        return positions or []

    @staticmethod
    def history_deals(date_from, date_to):
        deals = mt5.history_deals_get(date_from, date_to)
        return deals or []
