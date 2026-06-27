import streamlit as st


class V2Navigation:

    PAGES = {
        "Dashboard": {
            "icon": "🏠",
            "file": "pages/1_Dashboard.py",
            "group": "Home",
        },
        "Trade Review": {
            "icon": "📖",
            "file": "pages/2_Trade_Review.py",
            "group": "Trading",
        },
        "Analytics": {
            "icon": "📊",
            "file": "pages/3_Analytics.py",
            "group": "Trading",
        },
        "Strategy Builder": {
            "icon": "🎯",
            "file": "pages/4_Strategy_Builder.py",
            "group": "Trading",
        },
        "Research & AI": {
            "icon": "🤖",
            "file": "pages/5_Research_AI.py",
            "group": "Research",
        },
        "Automation": {
            "icon": "⚙️",
            "file": "pages/6_Automation.py",
            "group": "System",
        },
        "Settings": {
            "icon": "👤",
            "file": "pages/7_Settings.py",
            "group": "System",
        },
    }

    @staticmethod
    def sidebar():
        st.sidebar.markdown("## TradeHub V2")
        st.sidebar.caption("Professional Trading Journal")

        selected = st.sidebar.radio
