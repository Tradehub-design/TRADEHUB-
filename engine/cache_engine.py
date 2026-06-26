import streamlit as st

from core.config import AppConfig
from core.error_handler import ErrorHandler

from engine.trade_engine import TradeEngine


class CacheEngine:

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def trades():

        return ErrorHandler.execute(
            TradeEngine.load_all,
            default=None
        )

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def reviews():

        return ErrorHandler.execute(
            TradeEngine.load_reviews,
            default=None
        )

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def screenshots():

        return ErrorHandler.execute(
            TradeEngine.load_screenshots,
            default=None
        )

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def replays():

        return ErrorHandler.execute(
            TradeEngine.load_replays,
            default=None
        )

    @staticmethod
    def clear():

        st.cache_data.clear()
