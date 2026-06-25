import streamlit as st

from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe

from core.ui import load_css
from core.ui import app_header
from core.ui import section

from core.components import stat_row
from core.components import command_card

from research.queries import ResearchQueries

load_css()

app_header(
    "🔬 Research Lab",
    "Analyse your trading history and discover your edge."
)

supabase = get_supabase_client()

if supabase is None:
    st.stop()

response = (
    supabase.table("trades")
    .select("*")
    .order("trade_date", desc=True)
    .execute()
)

df = prepare_trades_dataframe(response.data)

if df.empty:

    command_card(
        "No trades",
        "Import trades before using Research Lab.",
        "Go to Import."
    )

    st.stop()

section("Research Filters")

symbols = ["All"] + sorted(df["symbol"].dropna().unique().tolist())

sessions = ["All"]

if "session" in df.columns:
    sessions += sorted(df["session"].dropna().unique().tolist())

col1, col2, col3 = st.columns(3)

with col1:

    symbol = st.selectbox(
        "Symbol",
        symbols
    )

with col2:

    session = st.selectbox(
        "Session",
        sessions
    )

with col3:

    result = st.selectbox(
        "Result",
        [
            "All",
            "Win",
            "Loss",
            "Breakeven"
        ]
    )

direction = st.selectbox(
    "Direction",
    [
        "All",
        "BUY",
        "SELL"
    ]
)

compare = st.selectbox(
    "Compare By",
    [
        None,
        "symbol",
        "session",
        "direction"
    ]
)

filtered, stats, comparison = ResearchQueries.run(
    df,
    symbol=symbol,
    session=session,
    direction=direction,
    result=result,
    compare_by=compare,
)

section("Research Summary")

stat_row([
    {
        "label":"Trades",
        "value":stats["total_trades"],
        "helper":"Filtered",
        "status":"neutral"
    },
    {
        "label":"Win %",
        "value":f'{stats["win_rate"]}%',
        "helper":"Win rate",
        "status":"positive"
    },
])

stat_row([
    {
        "label":"Net Profit",
        "value":stats["net_profit"],
        "helper":"Overall",
        "status":"positive" if stats["net_profit"] >= 0 else "negative"
    },
    {
        "label":"Profit Factor",
        "value":stats["profit_factor"],
        "helper":"Gross Profit / Gross Loss",
        "status":"positive"
    },
])

stat_row([
    {
        "label":"Average Win",
        "value":stats["average_win"],
        "helper":"Winning trades",
        "status":"positive"
    },
    {
        "label":"Average Loss",
        "value":stats["average_loss"],
        "helper":"Losing trades",
        "status":"negative"
    },
])

stat_row([
    {
        "label":"Expectancy",
        "value":stats["expectancy"],
        "helper":"Average expected outcome",
        "status":"neutral"
    }
])

section("Filtered Trades")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

if not comparison.empty:

    section("Comparison")

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )
