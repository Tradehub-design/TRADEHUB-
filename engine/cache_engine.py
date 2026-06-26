import streamlit as st

from core.config import AppConfig

from engine.trade_engine import TradeEngine


class CacheEngine:

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def trades():
        return TradeEngine.load_all()

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def reviews():
        return TradeEngine.load_reviews()

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def screenshots():
        return TradeEngine.load_screenshots()

    @staticmethod
    @st.cache_data(ttl=AppConfig.CACHE_TTL)
    def replays():
        return TradeEngine.load_replays()

    @staticmethod
    def clear():
        st.cache_data.clear()
