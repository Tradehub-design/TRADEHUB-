import streamlit as st


def account_filter(df):
    if df.empty or "account_number" not in df.columns:
        return df, "All Accounts"

    accounts = ["All Accounts"] + sorted(
        df["account_number"].dropna().astype(str).unique().tolist()
    )

    selected_account = st.selectbox("Account", accounts)

    if selected_account != "All Accounts":
        df = df[df["account_number"].astype(str) == selected_account]

    return df, selected_account


def trade_filters(df):
    if df.empty:
        return df

    col1, col2, col3 = st.columns(3)

    with col1:
        symbols = ["All"] + sorted(df["symbol"].dropna().unique().tolist())
        selected_symbol = st.selectbox("Symbol", symbols)

    with col2:
        strategies = ["All"] + sorted(df["strategy"].dropna().unique().tolist())
        selected_strategy = st.selectbox("Strategy", strategies)

    with col3:
        sessions = ["All"] + sorted(df["session"].dropna().unique().tolist())
        selected_session = st.selectbox("Session", sessions)

    if selected_symbol != "All":
        df = df[df["symbol"] == selected_symbol]

    if selected_strategy != "All":
        df = df[df["strategy"] == selected_strategy]

    if selected_session != "All":
        df = df[df["session"] == selected_session]

    return df
