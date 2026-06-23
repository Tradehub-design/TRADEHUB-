import streamlit as st
import pandas as pd
import plotly.express as px
from utils.supabase_client import get_supabase_client

st.subheader("📈 Equity Curve")

supabase = get_supabase_client()

response = supabase.table("trades").select("*").execute()

if response.data:

    df = pd.DataFrame(response.data)

    if "profit" in df.columns:

        df["cumulative_profit"] = df["profit"].cumsum()

        fig = px.line(
            df,
            y="cumulative_profit",
            title="Equity Curve"
        )

        st.plotly_chart(fig, use_container_width=True)
