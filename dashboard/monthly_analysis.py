import streamlit as st
import plotly.express as px


def show_monthly_analysis(df):
    st.subheader("🗓️ Monthly Performance")

    if df.empty or "trade_date" not in df.columns:
        st.info("No monthly data.")
        return

    temp = df.copy()
    temp["month"] = temp["trade_date"].dt.to_period("M").astype(str)

    result = (
        temp.groupby("month")
        .agg(net_profit=("net_profit", "sum"), trades=("ticket", "count"))
        .reset_index()
        .sort_values("month")
    )

    fig = px.bar(result, x="month", y="net_profit", text="trades")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
