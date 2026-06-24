import streamlit as st
import pandas as pd
from utils.supabase_client import get_supabase_client

st.title("📥 Import Trades")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

uploaded_file = st.file_uploader(
    "Upload MT5 / Fusion Markets CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview")
    st.dataframe(df.head(), use_container_width=True)

    account_number = st.text_input("Account Number", value="TEST001")

    if st.button("Import Trades"):
        imported = 0

        for _, row in df.iterrows():
            trade = {
                "ticket": int(row.get("ticket", row.get("Ticket", imported + 1))),
                "account_number": account_number,
                "symbol": row.get("symbol", row.get("Symbol", "")),
                "direction": row.get("direction", row.get("Type", "")),
                "volume": float(row.get("volume", row.get("Volume", 0))),
                "entry_price": float(row.get("entry_price", row.get("Price", 0))),
                "exit_price": float(row.get("exit_price", row.get("Close Price", 0))),
                "trade_date": row.get("trade_date", row.get("Time", None)),
                "profit": float(row.get("profit", row.get("Profit", 0))),
                "commission": float(row.get("commission", row.get("Commission", 0))),
                "swap": float(row.get("swap", row.get("Swap", 0))),
            }

            trade["net_profit"] = (
                trade["profit"]
                + trade["commission"]
                + trade["swap"]
            )

            supabase.table("trades").upsert(
                trade,
                on_conflict="ticket"
            ).execute()

            imported += 1

        st.success(f"Imported {imported} trades successfully.")
else:
    st.info("Upload a CSV file to begin.")
