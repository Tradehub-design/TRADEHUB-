import streamlit as st

from engine.trade_engine import TradeEngine


class CacheEngine:

    @staticmethod
    @st.cache_data(ttl=60)
    def trades():
        return TradeEngine.load_all()

    @staticmethod
    @st.cache_data(ttl=60)
    def reviews():
        return TradeEngine.load_reviews()

    @staticmethod
    @st.cache_data(ttl=60)
    def screenshots():
        return TradeEngine.load_screenshots()

    @staticmethod
    @st.cache_data(ttl=60)
    def replays():
        return TradeEngine.load_replays()
