import streamlit as st
import pandas as pd

from engine.format_engine import FormatEngine


class TradeTable:

    @staticmethod
    def prepare(df):
        if df is None or df.empty:
            return pd.DataFrame()

        table = df.copy()

        if "net_profit" in table.columns:
            table["Result"] = table["net_profit"].apply(
                FormatEngine.signed_currency
            )

        if "direction" in table.columns:
            table["Direction"] = table["direction"].astype(str).str.upper()

        if "symbol" in table.columns:
            table["Symbol"] = table["symbol"]

        if "ticket" in table.columns:
            table["Ticket"] = table["ticket"]

        if "trade_date" in table.columns:
            table["Close Time"] = table["trade_date"]

        if "session" in table.columns:
            table["Session"] = table["session"]

        cols = [
            col for col in [
                "Ticket",
                "Symbol",
                "Direction",
                "Result",
                "Close Time",
                "Session",
            ]
            if col in table.columns
        ]

        return table[cols]

    @staticmethod
    def render(df, height=520):
        table = TradeTable.prepare(df)

        if table.empty:
            st.info("No trades to display.")
            return

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            height=height
        )
