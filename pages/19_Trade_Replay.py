import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

from core.ui import load_css, app_header, section
from core.components import command_card, stat_row

from engine.edge_score import EdgeScoreEngine
from engine.grade import GradeEngine

from replay.replay_engine import ReplayEngine

load_css()

app_header(
    "🎬 Trade Replay",
    "Review every trade from beginning to end."
)

supabase = get_supabase_client()

trade_response = (
    supabase.table("trades")
    .select("*")
    .order("trade_date", desc=True)
    .execute()
)

review_response = (
    supabase.table("trade_journal_reviews")
    .select("*")
    .execute()
)

shot_response = (
    supabase.table("trade_screenshots")
    .select("*")
    .execute()
)

trades = prepare_trades_dataframe(trade_response.data)

reviews = pd.DataFrame(review_response.data)
shots = pd.DataFrame(shot_response.data)

if trades.empty:

    command_card(
        "No trades",
        "Import trades first.",
        "Go to Import."
    )

    st.stop()

trade_labels = []

for _, trade in trades.iterrows():

    trade_labels.append(
        f"{trade['ticket']} | {trade['symbol']} | {trade['net_profit']}"
    )

selected = st.selectbox(
    "Trade",
    trade_labels
)

ticket = int(selected.split("|")[0].strip())

trade = trades[
    trades["ticket"] == ticket
].iloc[0]

section("Trade")

stat_row([
    {
        "label":"Pair",
        "value":trade["symbol"],
        "helper":"Instrument",
        "status":"neutral"
    },
    {
        "label":"Profit",
        "value":trade["net_profit"],
        "helper":"Closed Result",
        "status":"positive" if trade["net_profit"]>=0 else "negative"
    }
])

review = reviews[
    reviews["trade_ticket"] == ticket
]

if not review.empty:

    review = review.iloc[0]

    edge = EdgeScoreEngine.calculate(
        review.to_dict(),
        trade.to_dict()
    )

    grade = GradeEngine.grade(edge)

    section("Execution")

    stat_row([
        {
            "label":"Edge Score",
            "value":edge,
            "helper":"Execution Quality",
            "status":"positive"
        },
        {
            "label":"Grade",
            "value":grade,
            "helper":"Overall",
            "status":"positive"
        }
    ])

section("Screenshot Timeline")

trade_shots = shots[
    shots["trade_ticket"] == ticket
]

if trade_shots.empty:

    st.info("No screenshots uploaded.")

else:

    for _, shot in trade_shots.iterrows():

        st.markdown(f"### {shot['screenshot_type']}")

        st.image(
            shot["public_url"],
            use_container_width=True
        )

        if shot["notes"]:
            st.caption(
                shot["notes"]
            )

section("Replay Notes")

summary = st.text_area(
    "Summary"
)

lessons = st.text_area(
    "Lessons Learned"
)

improvements = st.text_area(
    "What will you improve next time?"
)

if st.button("Save Replay"):

    payload = ReplayEngine.build_payload(
        ticket,
        trade["account_number"],
        summary,
        lessons,
        improvements
    )

    supabase.table(
        "trade_replays"
    ).upsert(
        payload,
        on_conflict="trade_ticket"
    ).execute()

    st.success(
        "Replay saved."
    )
