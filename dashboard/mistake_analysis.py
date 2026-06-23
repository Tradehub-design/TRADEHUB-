import streamlit as st
import plotly.express as px


def show_mistake_analysis(reviews):
    st.subheader("❌ Mistake Analysis")

    if reviews.empty or "mistake_type" not in reviews.columns:
        st.info("No mistake data.")
        return

    result = (
        reviews.groupby("mistake_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    fig = px.bar(result, x="mistake_type", y="count")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
