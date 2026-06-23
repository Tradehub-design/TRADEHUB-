import streamlit as st


def show_trade_card(trade, screenshots=None):
    screenshots = screenshots or []

    direction = trade.get("direction", "")
    symbol = trade.get("symbol", "")
    pnl = trade.get("net_profit", 0)
    pips = trade.get("pips", "")
    strategy = trade.get("strategy", "")
    session = trade.get("session", "")
    entry = trade.get("entry_price", "")
    exit_price = trade.get("exit_price", "")
    sl = trade.get("stop_loss", "")
    tp = trade.get("take_profit", "")
    notes = trade.get("notes", "")

    color = "🟩" if pnl and pnl > 0 else "🟥"

    with st.container(border=True):
        st.markdown(f"### {color} {symbol} {direction}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("P/L", pnl)
            st.write(f"**Pips:** {pips}")

        with col2:
            st.write(f"**Entry:** {entry}")
            st.write(f"**Exit:** {exit_price}")

        with col3:
            st.write(f"**SL:** {sl}")
            st.write(f"**TP:** {tp}")

        st.write(f"**Strategy:** {strategy}")
        st.write(f"**Session:** {session}")

        if notes:
            st.info(notes)

        if screenshots:
            st.write("**Screenshots**")
            cols = st.columns(min(len(screenshots), 3))

            for i, shot in enumerate(screenshots):
                image_url = shot.get("image_url")
                caption = shot.get("caption") or shot.get("timeframe") or "Screenshot"

                if image_url:
                    with cols[i % len(cols)]:
                        st.image(image_url, caption=caption, use_container_width=True)
