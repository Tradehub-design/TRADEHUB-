import streamlit as st


class V2Navigation:

    WORKSPACES = [
        "Dashboard",
        "Trade Review",
        "Analytics",
        "Strategy Builder",
        "Research & AI",
        "Automation",
        "Settings",
    ]

    ICONS = {
        "Dashboard": "🏠",
        "Trade Review": "📖",
        "Analytics": "📊",
        "Strategy Builder": "🎯",
        "Research & AI": "🤖",
        "Automation": "⚙️",
        "Settings": "👤",
    }

    @staticmethod
    def sidebar():
        with st.sidebar:
            st.markdown("## 📈 TradeHub")
            st.caption("Professional Trading Journal")

            selected = st.radio(
                "Navigation",
                V2Navigation.WORKSPACES,
                format_func=lambda item: f"{V2Navigation.ICONS[item]} {item}",
                label_visibility="collapsed",
            )

            st.divider()
            st.caption("TradeHub V2")

        return selected
