import streamlit as st
import plotly.express as px


def show_psychology_analysis(reviews):
    st.subheader("🧘 Psychology Analysis")

    if reviews.empty or "emotion_before" not in reviews.columns:
        st.info("No psychology data.")
        return

    result = (
        reviews.groupby("emotion_before")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    fig = px.bar(result, x="emotion_before", y="count")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(result, use_container_width=True)
