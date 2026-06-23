import streamlit as st
import plotly.express as px


def show_session_analysis(df):
    st.subheader("🕒 Session Performance")

    if df.empty or "session" not in df.columns:
        st.info("No session data.")
        return

    result = (
        df.groupby("session")
        .agg(net_profit=("net_profit", "sum"), trades=("ticket", "count"))
        .reset_index()
        .sort_values("net_profit", ascending=False)
    )

    fig = px.bar(result, x="session", y="net_profit", text="trades")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
