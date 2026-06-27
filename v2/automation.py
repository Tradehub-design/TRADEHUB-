import streamlit as st

from data.data_engine import DataEngine
from v2.ui import V2UI


class AutomationV2:

    @staticmethod
    def render():
        V2UI.header(
            "Automation",
            "MT5 sync, imports, screenshot watcher and system connections."
        )

        sync_status = DataEngine.load_sync_status()
        account_snapshot = DataEngine.load_account_snapshot()
        open_positions = DataEngine.load_open_positions()
        trades = DataEngine.load_trades()
        screenshots = DataEngine.load_screenshots()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "MT5 Sync",
            "Offline" if sync_status.empty else sync_status.iloc[0].get("status", "Unknown")
        )

        c2.metric(
            "Trades Loaded",
            0 if trades is None else len(trades)
        )

        c3.metric(
            "Open Positions",
            0 if open_positions is None else len(open_positions)
        )

        c4.metric(
            "Screenshots",
            0 if screenshots is None else len(screenshots)
        )

        tabs = st.tabs([
            "MT5 Sync",
            "Imports",
            "Screenshots",
            "TradingView",
            "System Health",
        ])

        with tabs[0]:
            V2UI.section("MT5 Desktop Sync")

            st.info(
                "Run the desktop sync agent on the same Windows computer as MT5."
            )

            st.code(
                "python desktop_sync/sync_agent.py",
                language="bash"
            )

            if not sync_status.empty:
                st.dataframe(
                    sync_status,
                    use_container_width=True,
                    hide_index=True
                )

            if not account_snapshot.empty:
                V2UI.section("Account Snapshot")
                st.dataframe(
                    account_snapshot,
                    use_container_width=True,
                    hide_index=True
                )

            if not open_positions.empty:
                V2UI.section("Open Positions")
                st.dataframe(
                    open_positions,
                    use_container_width=True,
                    hide_index=True
                )

        with tabs[1]:
            V2UI.section("Manual Imports")

            csv_file = st.file_uploader(
                "Upload CSV",
                type=["csv"]
            )

            if csv_file:
                st.success("CSV selected. Final importer will process this in the production setup.")

            st.file_uploader(
                "Upload Screenshots",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True
            )

        with tabs[2]:
            V2UI.section("Screenshot Watcher")

            st.info(
                "Place screenshots into your watched folder and the desktop watcher will upload them automatically."
            )

            st.code(
                "python desktop_sync/screenshot_watcher.py",
                language="bash"
            )

            if screenshots is None or screenshots.empty:
                st.warning("No screenshots found.")
            else:
                st.dataframe(
                    screenshots,
                    use_container_width=True,
                    hide_index=True
                )

        with tabs[3]:
            V2UI.section("TradingView Watcher")

            st.info(
                "TradingView screenshots will be watched from your configured folder and linked to trades."
            )

            st.code(
                "python automation/run_tradingview_watcher.py",
                language="bash"
            )

        with tabs[4]:
            V2UI.section("System Health")

            st.write("Database: Connected if data loads successfully.")
            st.write("MT5 Sync: Connected if sync_status is updated.")
            st.write("Screenshots: Connected if screenshot rows exist.")
            st.write("Desktop Agent: Must run locally on Windows.")
