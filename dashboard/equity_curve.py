import streamlit as st
import plotly.express as px


def show_equity_curve(df):
    if df.empty:
        st.info("No trades available for equity curve.")
        return

    if "trade_date" not in df.columns or "net_profit" not in df.columns:
        st.warning("Missing trade_date or net_profit columns.")
        return

    equity_df = df.sort_values("trade_date").copy()
    equity_df["cumulative_profit"] = equity_df["net_profit"].cumsum()

    fig = px.line(
        equity_df,
        x="trade_date",
        y="cumulative_profit",
        title="Equity Curve"
    )

    st.plotly_chart(fig, use_container_width=True)
