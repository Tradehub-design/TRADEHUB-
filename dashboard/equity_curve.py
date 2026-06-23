import streamlit as st
import plotly.express as px


def show_equity_curve(df):
    st.subheader("📈 Equity Curve")

    if df.empty:
        st.info("No trades available.")
        return

    df = df.sort_values("trade_date").copy()
    df["cumulative_profit"] = df["net_profit"].cumsum()

    fig = px.line(
        df,
        x="trade_date",
        y="cumulative_profit",
        title="Equity Curve"
    )

    st.plotly_chart(fig, use_container_width=True)
