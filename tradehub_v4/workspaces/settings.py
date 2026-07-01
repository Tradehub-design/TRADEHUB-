import streamlit as st
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI


class SettingsWorkspace:
    @staticmethod
    def render():
        UI.header("Settings", "Application configuration, trading defaults and data management.")
        tabs = st.tabs(["General", "Trading", "Accounts", "Database", "Appearance", "About"])
        with tabs[0]:
            st.text_input("App Name", value="TradeHub")
            st.text_input("Default Currency", value="AUD")
            if st.button("Clear Cache"):
                AppState.clear(); st.success("Cache cleared.")
        with tabs[1]:
            st.number_input("Default Risk %", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
            st.number_input("Max Trades Per Day", min_value=0, value=3, step=1)
            st.number_input("Stop After Losses", min_value=0, value=2, step=1)
            st.selectbox("Default Session", ["Asia", "London", "New York", "Any"])
        with tabs[2]:
            st.text_input("Broker", value="Fusion Markets")
            st.text_input("Default Account Name", value="Main Account")
            st.selectbox("Account Type", ["Live", "Demo", "Funded Challenge", "Funded Account", "Backtest"])
        with tabs[3]:
            st.text_input("Supabase URL")
            st.text_input("Supabase Key", type="password")
            st.button("Test Connection")
        with tabs[4]:
            st.toggle("Dark Mode", value=True)
            st.toggle("Compact Layout", value=False)
            st.selectbox("Accent Colour", ["Green", "Blue", "Purple", "Gold"])
        with tabs[5]:
            st.info("TradeHub V4 upload base: single-app trading command centre.")
            st.write("Version: V4.0 upload base")
