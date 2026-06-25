import streamlit as st
import pandas as pd

from utils.supabase_client import get_supabase_client
from research.data_loader import CandleLoader
from research.patterns import CandlePatterns
from research.backtester import ResearchBacktester
from research.statistics import ResearchStats
from research.storage import CandleStorage
from research.pattern_engine import PatternEngine
from research.pattern_registry import PATTERN_REGISTRY

st.title("🧪 Research Lab")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

st.write("Upload candle data once, save it, then reload it anytime for strategy research.")

symbol = st.text_input("Symbol", value="GBPJPY")

timeframe = st.selectbox(
    "Timeframe",
    ["1M", "5M", "15M", "30M", "1H", "4H", "1D"]
)

lookahead = st.slider("Lookahead candles", 1, 20, 5)

body_threshold = st.slider(
    "Continuation body threshold",
    0.1,
    0.95,
    0.6
)

st.divider()

st.subheader("Load Saved Candle Data")

if st.button("Load Saved Candles"):
    saved_df = CandleStorage.load_candles(supabase, symbol, timeframe)

    if saved_df.empty:
        st.warning("No saved candles found for this symbol/timeframe.")
        st.session_state["research_df"] = pd.DataFrame()
    else:
        st.session_state["research_df"] = saved_df
        st.success(f"Loaded {len(saved_df)} saved candles.")

st.divider()

st.subheader("Upload New Candle CSV")

uploaded_file = st.file_uploader(
    "Upload TradingView or MT5 candle CSV",
    type=["csv"]
)

if uploaded_file is not None:
    raw_df = CandleLoader.load_csv(uploaded_file)

    st.write("Raw preview")
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

    st.session_state["research_df"] = df

    if st.button("Save Uploaded Candles"):
        saved = CandleStorage.save_candles(supabase, df)
        st.success(f"Saved {saved} candles to Supabase.")

st.divider()

df = st.session_state.get("research_df", pd.DataFrame())

if df.empty:
    st.info("Load saved candles or upload a CSV to begin research.")
    st.stop()

st.subheader("Research Dataset")

st.write(f"Symbol: **{symbol}**")
st.write(f"Timeframe: **{timeframe}**")
st.write(f"Candles loaded: **{len(df)}**")

st.dataframe(df.head(20), use_container_width=True)

st.divider()

st.subheader("Pattern Research")

pattern_name = st.selectbox(
    "Choose Pattern",
    PatternEngine.get_available_patterns()
)

pattern_info = PATTERN_REGISTRY.get(pattern_name, {})

st.write(pattern_info.get("description", ""))

pattern_df = PatternEngine.run_pattern(
    df,
    pattern_name,
    {"body_threshold": body_threshold},
    CandlePatterns
)

bullish_signal = pattern_info.get("bullish_signal")
bearish_signal = pattern_info.get("bearish_signal")

bullish_results = ResearchBacktester.follow_through(
    pattern_df,
    bullish_signal,
    "bullish",
    lookahead
)

bearish_results = ResearchBacktester.follow_through(
    pattern_df,
    bearish_signal,
    "bearish",
    lookahead
)

col1, col2 = st.columns(2)

col1.metric(
    "Bullish Success",
    f"{ResearchStats.success_rate(bullish_results)}%"
)

col2.metric(
    "Bearish Success",
    f"{ResearchStats.success_rate(bearish_results)}%"
)

st.write("Bullish results")
st.dataframe(bullish_results.head(20), use_container_width=True)

st.write("Bearish results")
st.dataframe(bearish_results.head(20), use_container_width=True)
