import streamlit as st

from v2.navigation import V2Navigation
from v2.style import V2Style
from v2.dashboard import DashboardV2
from v2.trade_review import TradeReviewV2


st.set_page_config(
    page_title="TradeHub V2",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

V2Style.load()

selected = V2Navigation.sidebar()

if selected == "Dashboard":
    DashboardV2.render()
elif selected == "Trade Review":
    TradeReviewV2.render()
else:
    st.title(selected)
    st.info("This V2 workspace will be built next.")
