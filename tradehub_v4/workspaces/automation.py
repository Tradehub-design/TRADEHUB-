import streamlit as st
from tradehub_v4.core.state import AppState
from tradehub_v4.core.ui import UI


class AutomationWorkspace:
    @staticmethod
    def render():
        UI.header("Automation", "MT5 sync, imports, screenshots, TradingView and system health.")
        sync_status = AppState.sync_status()
        account = AppState.account_snapshot()
        open_positions = AppState.open_positions()
        screenshots = AppState.screenshots()
        trades = AppState.trades()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MT5 Sync", "Offline" if sync_status.empty else sync_status.iloc[0].get("status", "Unknown"))
        c2.metric("Trades Loaded", 0 if trades is None else len(trades))
        c3.metric("Open Positions", 0 if open_positions is None else len(open_positions))
        c4.metric("Screenshots", 0 if screenshots is None else len(screenshots))
        tabs = st.tabs(["MT5 Sync", "Imports", "Screenshots", "TradingView", "System Health"])
        with tabs[0]:
            st.info("Run this locally on the Windows computer with MT5 installed.")
            st.code("python desktop_sync/sync_agent.py", language="bash")
            if not sync_status.empty: st.dataframe(sync_status, use_container_width=True, hide_index=True)
            if not account.empty: st.dataframe(account, use_container_width=True, hide_index=True)
            if not open_positions.empty: st.dataframe(open_positions, use_container_width=True, hide_index=True)
        with tabs[1]:
            st.file_uploader("Upload CSV", type=["csv"])
            st.file_uploader("Upload screenshots", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
        with tabs[2]:
            st.code("python desktop_sync/screenshot_watcher.py", language="bash")
            if screenshots.empty: st.warning("No screenshots found.")
            else: st.dataframe(screenshots, use_container_width=True, hide_index=True)
        with tabs[3]:
            st.code("python automation/run_tradingview_watcher.py", language="bash")
        with tabs[4]:
            st.write("Database: Connected if data loads.")
            st.write("MT5 Sync: Connected if sync_status updates.")
            st.write("Desktop Agent: Runs locally on Windows.")
