import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row, table_header
from data.data_engine import DataEngine
from engine.statistics_engine import StatisticsEngine
from engine.account_type_engine import AccountTypeEngine
from engine.format_engine import FormatEngine
from components.trade_table import TradeTable


load_css()

app_header(
    "💼 Accounts",
    "Review account-level performance and live MT5 account status."
)

trades = DataEngine.load_trades()
account_snapshot = DataEngine.load_account_snapshot()
open_positions = DataEngine.load_open_positions()

section("Live Account")

if account_snapshot.empty:
    command_card(
        "No live account connected",
        "Run the MT5 Sync Agent to activate balance, equity and open-position tracking.",
        "Demo dataset is still available."
    )
else:
    account = account_snapshot.iloc[0]

    stat_row([
        {"label": "Balance", "value": account.get("balance", 0), "helper": "Live account", "status": "neutral"},
        {"label": "Equity", "value": account.get("equity", 0), "helper": "Live equity", "status": "positive" if account.get("equity", 0) >= account.get("balance", 0) else "negative"},
        {"label": "Floating P/L", "value": account.get("profit", 0), "helper": "Open positions", "status": "positive" if account.get("profit", 0) >= 0 else "negative"},
    ])

section("Account Performance")

if trades is None or trades.empty:
    command_card("No trades found", "Import trades first.", "Waiting for data.")
    st.stop()

trades = trades.copy()
trades["account_type"] = trades["account_number"].apply(AccountTypeEngine.classify)

account_type = st.selectbox("Account Type", AccountTypeEngine.options())

filtered = trades.copy()

if account_type != "All":
    filtered = filtered[filtered["account_type"] == account_type]

stats = StatisticsEngine.summary(filtered)

stat_row([
    {"label": "Trades", "value": stats["total_trades"], "helper": account_type, "status": "neutral"},
    {"label": "Net Profit", "value": FormatEngine.signed_currency(stats["net_profit"]), "helper": "Closed result", "status": FormatEngine.result_status(stats["net_profit"])},
    {"label": "Win Rate", "value": f"{stats['win_rate']}%", "helper": "Wins", "status": "positive" if stats["win_rate"] >= 50 else "negative"},
])

section("Open Positions")

if open_positions.empty:
    command_card("No open positions", "Open trades will appear after MT5 Sync runs.", "Live monitoring.")
else:
    table_header("Open Positions", f"{len(open_positions)} active positions")
    st.dataframe(open_positions, use_container_width=True, hide_index=True)

section("Account Trades")

TradeTable.render(filtered, height=520)
