import streamlit as st
import plotly.express as px


def show_drawdown_analysis(df):

    st.subheader("📉 Drawdown")

    if df.empty:
        return

    dd = df.sort_values("trade_date").copy()

    dd["equity"] = dd["net_profit"].cumsum()
    dd["peak"] = dd["equity"].cummax()
    dd["drawdown"] = dd["equity"] - dd["peak"]

    max_dd = round(dd["drawdown"].min(), 2)

    st.metric("Max Drawdown", max_dd)

    fig = px.line(
        dd,
        x="trade_date",
        y="drawdown",
        title="Drawdown Curve"
    )

    st.plotly_chart(fig, use_container_width=True)
