import streamlit as st

from core.ui import load_css, app_header, section
from core.components import table_header, command_card
from data.data_engine import DataEngine
from engine.replay_engine import ReplayEngine

load_css()

app_header(
    "▶ Replay Centre",
    "Replay every trade exactly how it happened."
)

trades = DataEngine.load_trades()

screenshots = DataEngine.load_screenshots()

if trades.empty:

    command_card(
        "No trades",
        "Import trades first.",
        ""
    )

    st.stop()

ticket = st.selectbox(

    "Trade",

    trades["ticket"]

)

trade = trades[
    trades.ticket == ticket
].iloc[0]

timeline = ReplayEngine.build_timeline(

    trade,

    screenshots

)

section("Replay Timeline")

st.dataframe(

    timeline,

    hide_index=True,

    use_container_width=True

)

section("Replay Images")

command_card(

    "Replay Images",

    "Screenshots connected to this trade will appear here.",

    "Screenshot automation coming shortly."

)
