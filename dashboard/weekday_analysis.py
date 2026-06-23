import streamlit as st
import plotly.express as px


def show_weekday_analysis(df):
    st.subheader("📆 Weekday Performance")

    if df.empty or "trade_date" not in df.columns:
        st.info("No weekday data.")
        return

    temp = df.copy()
    temp["weekday"] = temp["trade_date"].dt.day_name()

    result = (
        temp.groupby("weekday")
        .agg(net_profit=("net_profit", "sum"), trades=("ticket", "count"))
        .reset_index()
    )

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    result["weekday"] = result["weekday"].astype("category")
    result["weekday"] = result["weekday"].cat.set_categories(order)
    result = result.sort_values("weekday")

    fig = px.bar(result, x="weekday", y="net_profit", text="trades")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
