import streamlit as st


def load_css():
    try:
        with open("assets/styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def app_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def metric(label, value, helper="", status="neutral"):
    status_class = {
        "positive": "metric-positive",
        "negative": "metric-negative",
        "neutral": "metric-neutral",
    }.get(status, "metric-neutral")

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value {status_class}">{value}</div>
            <div class="metric-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight(title, body):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def badge(text):
    st.markdown(
        f'<span class="badge">{text}</span>',
        unsafe_allow_html=True
    )
