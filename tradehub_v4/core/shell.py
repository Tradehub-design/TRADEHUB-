import streamlit as st

WORKSPACES = [
    "Dashboard",
    "Trade Reviews",
    "Analytics",
    "Strategies",
    "Research & AI",
    "Automation",
    "Settings",
]

ICONS = {
    "Dashboard": "🏠",
    "Trade Reviews": "📖",
    "Analytics": "📊",
    "Strategies": "🎯",
    "Research & AI": "🤖",
    "Automation": "⚙️",
    "Settings": "👤",
}


def render_shell():
    with st.sidebar:
        st.markdown("# 📈 TradeHub")
        st.caption("V4 Trading Command Centre")
        selected = st.radio(
            "Navigation",
            WORKSPACES,
            format_func=lambda item: f"{ICONS[item]} {item}",
            label_visibility="collapsed",
        )
        st.divider()
        st.caption("Single-app mode • V4.0 base")
    return selected
