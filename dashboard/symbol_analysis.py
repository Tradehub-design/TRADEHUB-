import streamlit as st
import plotly.express as px


def show_symbol_analysis(df):
    if df.empty or "symbol" not in df.columns:
        return

    st.subheader("📌 Symbol Performance")

    symbol_df = (
        df.groupby("symbol")
        .agg(
            net_profit=("net_profit", "sum"),
            trades=("ticket", "count")
        )
        .reset_index()
        .sort_values("net_profit", ascending=False)
    )

    fig = px.bar(
        symbol_df,
        x="symbol",
        y="net_profit",
        text="trades",
        title="Profit by Symbol"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(symbol_df, use_container_width=True)
