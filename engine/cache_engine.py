import pandas as pd
import streamlit as st

from core.config import AppConfig
from core.logger import Logger
from engine.trade_engine import TradeEngine
from engine.live_engine import LiveEngine


class CacheEngine:

    @staticmethod
    def _safe_load(loader):
        try:
            result = loader()

            if result is None:
                return pd.DataFrame()

            return result

        except Exception as e:
            Logger.exception(str(e))
            return pd.DataFrame()

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def trades():
        return CacheEngine._safe_load(TradeEngine.load_all)

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def reviews():
        return CacheEngine._safe_load(TradeEngine.load_reviews)

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def screenshots():
        return CacheEngine._safe_load(TradeEngine.load_screenshots)

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def replays():
        return CacheEngine._safe_load(TradeEngine.load_replays)

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def account_snapshot():
        return CacheEngine._safe_load(LiveEngine.account_snapshot)

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def open_positions():
        return CacheEngine._safe_load(LiveEngine.open_positions)

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def sync_status():
        return CacheEngine._safe_load(LiveEngine.sync_status)

    @staticmethod
    def clear():
        st.cache_data.clear()
