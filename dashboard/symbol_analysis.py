import streamlit as st
import plotly.express as px


def show_symbol_analysis(df):
    st.subheader("📌 Symbol Performance")

    if df.empty or "symbol" not in df.columns:
        st.info("No symbol data.")
        return

    result = (
        df.groupby("symbol")
        .agg(net_profit=("net_profit", "sum"), trades=("ticket", "count"))
        .reset_index()
        .sort_values("net_profit", ascending=False)
    )

    fig = px.bar(result, x="symbol", y="net_profit", text="trades")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
