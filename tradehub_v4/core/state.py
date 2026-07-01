import streamlit as st
from data.data_engine import DataEngine


class AppState:
    @staticmethod
    @st.cache_data(ttl=60)
    def trades():
        return DataEngine.load_trades()

    @staticmethod
    @st.cache_data(ttl=60)
    def reviews():
        return DataEngine.load_reviews()

    @staticmethod
    @st.cache_data(ttl=60)
    def screenshots():
        return DataEngine.load_screenshots()

    @staticmethod
    @st.cache_data(ttl=60)
    def replays():
        return DataEngine.load_replays()

    @staticmethod
    @st.cache_data(ttl=60)
    def account_snapshot():
        return DataEngine.load_account_snapshot()

    @staticmethod
    @st.cache_data(ttl=60)
    def open_positions():
        return DataEngine.load_open_positions()

    @staticmethod
    @st.cache_data(ttl=60)
    def sync_status():
        return DataEngine.load_sync_status()

    @staticmethod
    def clear():
        st.cache_data.clear()
