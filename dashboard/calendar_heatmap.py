import streamlit as st


def show_calendar_heatmap(daily):

    st.subheader("📅 Trading Calendar")

    for _, row in daily.iterrows():

        pnl = round(row["pnl"], 2)

        if pnl >= 0:
            color = "🟩"
        else:
            color = "🟥"

        st.markdown(
            f"""
            {color} **{row['trade_date']}**

            P/L: {pnl}

            Trades: {row['trades']}

            ---
            """
        )
