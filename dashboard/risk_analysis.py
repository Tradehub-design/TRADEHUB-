import streamlit as st


def show_risk_analysis(df):

    st.subheader("⚠️ Risk Analysis")

    if df.empty:
        return

    avg_rr = (
        round(df["actual_rr"].mean(), 2)
        if "actual_rr" in df.columns
        else 0
    )

    avg_risk = (
        round(df["risk_percent"].mean(), 2)
        if "risk_percent" in df.columns
        else 0
    )

    col1, col2 = st.columns(2)

    col1.metric("Average R", avg_rr)
    col2.metric("Average Risk %", avg_risk)
