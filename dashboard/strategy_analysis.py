import streamlit as st
import plotly.express as px


def show_strategy_analysis(df):
    st.subheader("🧠 Strategy Performance")

    if df.empty or "strategy" not in df.columns:
        st.info("No strategy data.")
        return

    result = (
        df.groupby("strategy")
        .agg(net_profit=("net_profit", "sum"), trades=("ticket", "count"))
        .reset_index()
        .sort_values("net_profit", ascending=False)
    )

    fig = px.bar(result, x="strategy", y="net_profit", text="trades")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
