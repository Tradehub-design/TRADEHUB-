import streamlit as st
import plotly.express as px


def show_account_analysis(df):

    st.subheader("🏦 Account Performance")

    if df.empty:
        return

    result = (
        df.groupby("account_number")
        .agg(
            net_profit=("net_profit", "sum"),
            trades=("ticket", "count")
        )
        .reset_index()
    )

    fig = px.bar(
        result,
        x="account_number",
        y="net_profit",
        text="trades"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(result, use_container_width=True)
