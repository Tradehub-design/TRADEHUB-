import streamlit as st

from tradehub_v4.core.style import load_style
from tradehub_v4.core.shell import render_shell
from tradehub_v4.workspaces.dashboard import DashboardWorkspace
from tradehub_v4.workspaces.trade_reviews import TradeReviewsWorkspace
from tradehub_v4.workspaces.analytics import AnalyticsWorkspace
from tradehub_v4.workspaces.strategies import StrategiesWorkspace
from tradehub_v4.workspaces.research_ai import ResearchAIWorkspace
from tradehub_v4.workspaces.automation import AutomationWorkspace
from tradehub_v4.workspaces.settings import SettingsWorkspace

st.set_page_config(
    page_title="TradeHub V4",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_style()
workspace = render_shell()

if workspace == "Dashboard":
    DashboardWorkspace.render()
elif workspace == "Trade Reviews":
    TradeReviewsWorkspace.render()
elif workspace == "Analytics":
    AnalyticsWorkspace.render()
elif workspace == "Strategies":
    StrategiesWorkspace.render()
elif workspace == "Research & AI":
    ResearchAIWorkspace.render()
elif workspace == "Automation":
    AutomationWorkspace.render()
elif workspace == "Settings":
    SettingsWorkspace.render()
