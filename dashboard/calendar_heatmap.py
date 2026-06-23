import streamlit as st


def show_calendar_heatmap(daily):
    st.subheader("📅 Trading Calendar")

    if daily.empty:
        st.info("No calendar data.")
        return

    for _, row in daily.iterrows():

        pnl = round(row["pnl"], 2)
        trades = row["trades"]
        date = row["trade_date"]

        color = "🟩" if pnl >= 0 else "🟥"

        st.markdown(
            f"""
            {color} **{date}**

            P/L: {pnl}

            Trades: {trades}

            ---
            """
        )
