import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

from core.ui import load_css, app_header, section
from core.components import stat_row, command_card

from engine.analytics_engine import AnalyticsEngine


load_css()

app_header(
    "📊 Analytics Pro",
    "Understand your strongest symbols, sessions, months and trading performance."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

trade_response = (
    supabase.table("trades")
    .select("*")
    .order("trade_date", desc=True)
    .execute()
)

df = prepare_trades_dataframe(trade_response.data)

if df.empty:
    command_card(
        "No trades found",
        "Import trades before using Analytics Pro.",
        "Go to Import."
    )
    st.stop()

section("Overall Summary")

wins = df[df["net_profit"] > 0]
losses = df[df["net_profit"] < 0]

total_trades = len(df)
net_profit = round(df["net_profit"].sum(), 2)
win_rate = round((len(wins) / total_trades) * 100, 2) if total_trades else 0
average_trade = round(df["net_profit"].mean(), 2)

stat_row([
    {
        "label": "Total Trades",
        "value": total_trades,
        "helper": "Imported trades",
        "status": "neutral",
    },
    {
        "label": "Net Profit",
        "value": net_profit,
        "helper": "Total closed result",
        "status": "positive" if net_profit >= 0 else "negative",
    },
])

stat_row([
    {
        "label": "Win Rate",
        "value": f"{win_rate}%",
        "helper": "Winning trades / all trades",
        "status": "positive" if win_rate >= 50 else "negative",
    },
    {
        "label": "Avg Trade",
        "value": average_trade,
        "helper": "Average result per trade",
        "status": "positive" if average_trade >= 0 else "negative",
    },
])

section("Symbol Leaderboard")

symbol_df = AnalyticsEngine.symbol_summary(df)

if symbol_df.empty:
    st.info("No symbol data available.")
else:
    st.dataframe(
        symbol_df,
        use_container_width=True,
        hide_index=True
    )

section("Session Leaderboard")

session_df = AnalyticsEngine.session_summary(df)

if session_df.empty:
    st.info("No session data available.")
else:
    st.dataframe(
        session_df,
        use_container_width=True,
        hide_index=True
    )

section("Monthly Performance")

monthly_df = AnalyticsEngine.monthly_summary(df)

if monthly_df.empty:
    st.info("No monthly data available.")
else:
    st.line_chart(
        monthly_df.set_index("Month")["NetProfit"]
    )

    st.dataframe(
        monthly_df,
        use_container_width=True,
        hide_index=True
    )

section("Best / Worst")

if not symbol_df.empty:
    best_symbol = symbol_df.iloc[0]
    worst_symbol = symbol_df.iloc[-1]

    stat_row([
        {
            "label": "Best Symbol",
            "value": best_symbol["symbol"],
            "helper": f'Net: {round(best_symbol["NetProfit"], 2)}',
            "status": "positive",
        },
        {
            "label": "Worst Symbol",
            "value": worst_symbol["symbol"],
            "helper": f'Net: {round(worst_symbol["NetProfit"], 2)}',
            "status": "negative",
        },
    ])

if not session_df.empty:
    best_session = session_df.iloc[0]
    worst_session = session_df.iloc[-1]

    stat_row([
        {
            "label": "Best Session",
            "value": best_session["session"],
            "helper": f'Net: {round(best_session["NetProfit"], 2)}',
            "status": "positive",
        },
        {
            "label": "Worst Session",
            "value": worst_session["session"],
            "helper": f'Net: {round(worst_session["NetProfit"], 2)}',
            "status": "negative",
        },
    ])
