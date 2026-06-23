import streamlit as st

def show_equity_curve(df):
    st.subheader("📈 Equity Curve")

    if df.empty:
        st.info("No trades available.")
        return

    equity_df = df.sort_values("trade_date").copy()
    equity_df["cumulative_profit"] = equity_df["net_profit"].cumsum()

    chart_df = equity_df.set_index("trade_date")[["cumulative_profit"]]

    st.line_chart(chart_df)
