import streamlit as st

from v2.style import V2Style
from v2.shell import TradeHubShell
from v2.workspaces.dashboard import DashboardWorkspace
from v2.workspaces.trade_review import TradeReviewWorkspace
from v2.workspaces.analytics import AnalyticsWorkspace
from v2.workspaces.strategy_builder import StrategyBuilderWorkspace
from v2.workspaces.research_ai import ResearchAIWorkspace
from v2.workspaces.automation import AutomationWorkspace
from v2.workspaces.settings import SettingsWorkspace


st.set_page_config(
    page_title="TradeHub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

V2Style.load()

workspace = TradeHubShell.sidebar()

if workspace == "Dashboard":
   
