import streamlit as st

from v2.ui import V2UI


class SettingsV2:

    @staticmethod
    def render():
        V2UI.header(
            "Settings",
            "Application configuration, trading defaults and appearance."
        )

        tabs = st.tabs([
            "General",
            "Trading",
            "Accounts",
            "Database",
            "Appearance",
            "About",
        ])

        with tabs[0]:
            V2UI.section("General")

            st.text_input(
                "App Name",
                value="TradeHub"
            )

            st.text_input(
                "Default Currency",
                value="AUD"
            )

        with tabs[1]:
            V2UI.section("Trading Defaults")

            st.number_input(
                "Default Risk %",
                min_value=0.0,
                max_value=100.0,
                value=1.0,
                step=0.1,
            )

            st.number_input(
                "Max Trades Per Day",
                min_value=0,
                value=3,
                step=1,
            )

            st.number_input(
                "Stop After Losses",
                min_value=0,
                value=2,
                step=1,
            )

            st.selectbox(
                "Default Session",
                [
                    "Asia",
                    "London",
                    "New York",
                    "Any",
                ],
            )

        with tabs[2]:
            V2UI.section("Accounts")

            st.text_input(
                "Broker",
                value="Fusion Markets"
            )

            st.text_input(
                "Default Account Name",
                value="Main Account"
            )

            st.selectbox(
                "Account Type",
                [
                    "Live",
                    "Demo",
                    "Funded Challenge",
                    "Funded Account",
                    "Backtest",
                ],
            )

        with tabs[3]:
            V2UI.section("Database")

            st.text_input(
                "Supabase URL",
                placeholder="https://your-project.supabase.co"
            )

            st.text_input(
                "Supabase Key",
                type="password"
            )

            st.button("Test Connection")

        with tabs[4]:
            V2UI.section("Appearance")

            st.toggle(
                "Dark Mode",
                value=True
            )

            st.toggle(
                "Compact Layout",
                value=False
            )

            st.selectbox(
                "Accent Colour",
                [
                    "Green",
                    "Blue",
                    "Purple",
                    "Gold",
                ],
            )

        with tabs[5]:
            V2UI.section("About TradeHub")

            st.info(
                "TradeHub V2 is a simplified single-app trading journal built around Dashboard, Trade Review, Analytics, Strategy Builder, Research & AI, Automation and Settings."
            )

            st.write("Version: V2.0")
