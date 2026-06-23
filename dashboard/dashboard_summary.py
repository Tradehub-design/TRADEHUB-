import streamlit as st


def show_dashboard_summary(stats):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Trades", stats.get("total_trades", 0))
    col2.metric("Net Profit", stats.get("net_profit", 0))
    col3.metric("Wins", stats.get("wins", 0))
    col4.metric("Win Rate", f"{stats.get('win_rate', 0)}%")
