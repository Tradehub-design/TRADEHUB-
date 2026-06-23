import streamlit as st
from utils.supabase_client import get_supabase_client
from utils.analytics_utils import prepare_trades_dataframe, prepare_reviews_dataframe
from dashboard.filter_panel import account_filter, trade_filters
from dashboard.symbol_analysis import show_symbol_analysis
from dashboard.session_analysis import show_session_analysis
from dashboard.strategy_analysis import show_strategy_analysis
from dashboard.weekday_analysis import show_weekday_analysis
from dashboard.monthly_analysis import show_monthly_analysis
from dashboard.drawdown_analysis import show_drawdown_analysis
from dashboard.risk_analysis import show_risk_analysis
from dashboard.account_analysis import show_account_analysis
from dashboard.mistake_analysis import show_mistake_analysis
from dashboard.psychology_analysis import show_psychology_analysis

st.title("📊 Analytics")

supabase = get_supabase_client()

if supabase is None:
    st.stop()

trade_response = supabase.table("trades").select("*").execute()
review_response = supabase.table("trade_reviews").select("*").execute()

df = prepare_trades_dataframe(trade_response.data)
reviews = prepare_reviews_dataframe(review_response.data)

if df.empty:
    st.info("No trades found yet.")
    st.stop()

df, selected_account = account_filter(df)
df = trade_filters(df)

show_symbol_analysis(df)
st.divider()

show_session_analysis(df)
st.divider()

show_strategy_analysis(df)
st.divider()

show_weekday_analysis(df)
st.divider()

show_monthly_analysis(df)
st.divider()

show_drawdown_analysis(df)
st.divider()

show_risk_analysis(df)
st.divider()

show_account_analysis(df)
st.divider()

show_mistake_analysis(reviews)
st.divider()

show_psychology_analysis(reviews)
