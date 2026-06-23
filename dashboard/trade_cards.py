import streamlit as st


def show_trade_card(trade, screenshots=None):

    screenshots = screenshots or []

    pnl = trade.get("net_profit", 0)

    color = "🟩" if pnl > 0 else "🟥"

    with st.container(border=True):

        st.markdown(
            f"### {color} {trade.get('symbol')} {trade.get('direction')}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("P/L", pnl)
            st.write(f"Pips: {trade.get('pips', '')}")

        with col2:
            st.write(f"Entry: {trade.get('entry_price', '')}")
            st.write(f"Exit: {trade.get('exit_price', '')}")

        with col3:
            st.write(f"SL: {trade.get('stop_loss', '')}")
            st.write(f"TP: {trade.get('take_profit', '')}")

        st.write(f"Strategy: {trade.get('strategy', '')}")
        st.write(f"Session: {trade.get('session', '')}")

        if trade.get("notes"):
            st.info(trade["notes"])

        if screenshots:

            cols = st.columns(min(3, len(screenshots)))

            for i, shot in enumerate(screenshots):

                image_url = shot.get("image_url")

                if image_url:

                    with cols[i % len(cols)]:

                        st.image(
                            image_url,
                            caption=shot.get(
                                "caption",
                                shot.get("timeframe", "Screenshot")
                            ),
                            use_container_width=True
                        )
