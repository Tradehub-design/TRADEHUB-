import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from research.data_loader import CandleLoader
from research.patterns import CandlePatterns
from research.backtester import ResearchBacktester
from research.statistics import ResearchStats
from research.storage import CandleStorage

st.title("🧪 Research Lab")

st.write("Upload candle data and test trading ideas like liquidity sweeps and continuation candles.")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

uploaded_file = st.file_uploader(
    "Upload candle CSV",
    type=["csv"]
)

symbol = st.text_input("Symbol", value="GBPJPY")
timeframe = st.selectbox(
    "Timeframe",
    ["1M", "5M", "15M", "30M", "1H", "4H", "1D"]
)

lookahead = st.slider(
    "Lookahead candles",
    1,
    20,
    5
)

body_threshold = st.slider(
    "Continuation body threshold",
    0.1,
    0.95,
    0.6
)

if uploaded_file is None:
    st.info("Upload a TradingView or MT5 candle CSV to begin.")
    st.stop()

raw_df = CandleLoader.load_csv(uploaded_file)

st.subheader("Raw Preview")
st.dataframe(raw_df.head(), use_container_width=True)

columns = CandleLoader.detect_columns(raw_df)

required = [
    columns["time"],
    columns["open"],
    columns["high"],
    columns["low"],
    columns["close"],
]

if any(col is None for col in required):
    st.error("Could not detect required candle columns.")
    st.write(columns)
    st.stop()

df = pd.DataFrame({
    "symbol": symbol,
    "timeframe": timeframe,
    "candle_time": pd.to_datetime(raw_df[columns["time"]]),
    "open_price": pd.to_numeric(raw_df[columns["open"]], errors="coerce"),
    "high_price": pd.to_numeric(raw_df[columns["high"]], errors="coerce"),
    "low_price": pd.to_numeric(raw_df[columns["low"]], errors="coerce"),
    "close_price": pd.to_numeric(raw_df[columns["close"]], errors="coerce"),
    "volume": pd.to_numeric(raw_df[columns["volume"]], errors="coerce") if columns["volume"] else 0,
})

df = df.dropna(
    subset=[
        "candle_time",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
    ]
)

st.success(f"Detected {len(df)} candles.")

if st.button("Save Candles"):
    saved = CandleStorage.save_candles(supabase, df)
    st.success(f"Saved {saved} candles.")

st.divider()

st.subheader("Liquidity Sweep Research")

sweep_df = CandlePatterns.liquidity_sweeps(df)

bullish_results = ResearchBacktester.follow_through(
    sweep_df,
    "bullish_sweep",
    "bullish",
    lookahead
)

bearish_results = ResearchBacktester.follow_through(
    sweep_df,
    "bearish_sweep",
    "bearish",
    lookahead
)

col1, col2 = st.columns(2)

col1.metric(
    "Bullish Sweep Success",
    f"{ResearchStats.success_rate(bullish_results)}%"
)

col2.metric(
    "Bearish Sweep Success",
    f"{ResearchStats.success_rate(bearish_results)}%"
)

st.write("Bullish sweep results")
st.dataframe(bullish_results.head(20), use_container_width=True)

st.write("Bearish sweep results")
st.dataframe(bearish_results.head(20), use_container_width=True)

st.divider()

st.subheader("Continuation Candle Research")

cont_df = CandlePatterns.continuation(
    df,
    body_threshold
)

bull_cont_results = ResearchBacktester.follow_through(
    cont_df,
    "bullish",
    "bullish",
    lookahead
)

bear_cont_results = ResearchBacktester.follow_through(
    cont_df,
    "bearish",
    "bearish",
    lookahead
)

col3, col4 = st.columns(2)

col3.metric(
    "Bullish Continuation Success",
    f"{ResearchStats.success_rate(bull_cont_results)}%"
)

col4.metric(
    "Bearish Continuation Success",
    f"{ResearchStats.success_rate(bear_cont_results)}%"
)

st.write("Bullish continuation results")
st.dataframe(bull_cont_results.head(20), use_container_width=True)

st.write("Bearish continuation results")
st.dataframe(bear_cont_results.head(20), use_container_width=True)
