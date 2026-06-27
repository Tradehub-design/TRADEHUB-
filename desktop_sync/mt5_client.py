from datetime import datetime, timedelta

import MetaTrader5 as mt5

from desktop_sync.config import DesktopSyncConfig
from desktop_sync.logger import DesktopLogger


class MT5Client:

    @staticmethod
    def connect():
        if not mt5.initialize():
            raise Exception(f"MT5 initialize failed: {mt5.last_error()}")

        if (
            DesktopSyncConfig.MT5_LOGIN
            and DesktopSyncConfig.MT5_PASSWORD
            and DesktopSyncConfig.MT5_SERVER
        ):
            logged_in = mt5.login(
                login=int(DesktopSyncConfig.MT5_LOGIN),
                password=DesktopSyncConfig.MT5_PASSWORD,
                server=DesktopSyncConfig.MT5_SERVER,
            )

            if not logged_in:
                raise Exception(f"MT5 login failed: {mt5.last_error()}")

        DesktopLogger.info("MT5 connected")
        return True

    @staticmethod
    def disconnect():
        mt5.shutdown()
        DesktopLogger.info("MT5 disconnected")

    @staticmethod
    def account_info():
        return mt5.account_info()

    @staticmethod
    def open_positions():
        return mt5.positions_get() or []

    @staticmethod
    def history_deals():
        date_to = datetime.now()
        date_from = date_to - timedelta(
            days=DesktopSyncConfig.HISTORY_DAYS_BACK
        )

        return mt5.history_deals_get(date_from, date_to) or []
