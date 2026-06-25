import streamlit as st
import pandas as pd
from utils.supabase_client import get_supabase_client

st.title("📥 Import Trades")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

uploaded_file = st.file_uploader(
    "Upload MT5 detailed report CSV / HTML",
    type=["csv", "html", "htm"]
)

account_number = st.text_input("Account Number", value="9069610")


def clean_number(value):
    try:
        if pd.isna(value):
            return 0
        return float(str(value).replace(",", "").replace(" ", ""))
    except Exception:
        return 0


def normalise_columns(df):
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return df


def extract_trades_from_file(file):
    name = file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(file)
        return normalise_columns(df)

    if name.endswith(".html") or name.endswith(".htm"):
        tables = pd.read_html(file)

        best_table = None

        for table in tables:
            cols = [str(c).lower() for c in table.columns]
            joined = " ".join(cols)

            if (
                "time" in joined
                and ("profit" in joined or "symbol" in joined)
            ):
                best_table = table
                break

        if best_table is None:
            st.error("Could not find a trade table in this HTML report.")
            return pd.DataFrame()

        return normalise_columns(best_table)

    return pd.DataFrame()


if uploaded_file is not None:
    df = extract_trades_from_file(uploaded_file)

    if df.empty:
        st.stop()

    st.subheader("Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.write("Detected columns:")
    st.write(list(df.columns))

    if st.button("Import Trades"):
        imported = 0

        for i, row in df.iterrows():
            ticket = row.get("ticket", row.get("position", row.get("order", i + 1)))
            symbol = row.get("symbol", "")
            direction = row.get("type", row.get("direction", ""))

            trade = {
                "ticket": int(clean_number(ticket)),
                "account_number": str(account_number),
                "symbol": str(symbol),
                "direction": str(direction).upper(),
                "volume": clean_number(row.get("volume", row.get("size", 0))),
                "entry_price": clean_number(row.get("price", row.get("entry_price", 0))),
                "exit_price": clean_number(row.get("close_price", row.get("exit_price", 0))),
                "trade_date": row.get("time", row.get("close_time", row.get("date", None))),
                "profit": clean_number(row.get("profit", 0)),
                "commission": clean_number(row.get("commission", 0)),
                "swap": clean_number(row.get("swap", 0)),
                "net_profit": (
                    clean_number(row.get("profit", 0))
                    + clean_number(row.get("commission", 0))
                    + clean_number(row.get("swap", 0))
                ),
            }

            if trade["ticket"] == 0:
                continue

            supabase.table("trades").upsert(
                trade,
                on_conflict="ticket"
            ).execute()

            imported += 1

        st.success(f"Imported {imported} trades.")
else:
    st.info("Upload an MT5 detailed report CSV or HTML file.")
