import streamlit as st


def command_card(title, body, footer=""):
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
            <div class="card-footer">{footer}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def feature_card(title, body, tag=""):
    tag_html = f'<span class="tradehub-badge">{tag}</span>' if tag else ""

    st.markdown(
        f"""
        <div class="premium-card">
            {tag_html}
            <div class="card-title">{title}</div>
            <div class="card-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def stat_row(items):
    columns = st.columns(len(items))

    for col, item in zip(columns, items):
        with col:
            status = item.get("status", "neutral")
            status_class = {
                "positive": "metric-positive",
                "negative": "metric-negative",
                "neutral": "metric-neutral",
                "warning": "metric-warning",
            }.get(status, "metric-neutral")

            st.markdown(
                f"""
                <div class="premium-card metric-card">
                    <div class="metric-label">{item.get("label", "")}</div>
                    <div class="metric-value {status_class}">
                        {item.get("value", "-")}
                    </div>
                    <div class="metric-helper">{item.get("helper", "")}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


def trade_quality_card(score, helper=""):
    if score >= 85:
        status = "metric-positive"
        label = "Strong Edge"
    elif score >= 70:
        status = "metric-warning"
        label = "Moderate Edge"
    else:
        status = "metric-negative"
        label = "Weak Edge"

    st.markdown(
        f"""
        <div class="premium-card edge-card">
            <div class="metric-label">Trade Quality</div>
            <div class="edge-score {status}">{score}</div>
            <div class="metric-helper">{label}</div>
            <div class="metric-helper">{helper}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def status_badge(text, status="neutral"):
    status_class = {
        "positive": "badge-positive",
        "negative": "badge-negative",
        "warning": "badge-warning",
        "neutral": "badge-neutral",
    }.get(status, "badge-neutral")

    st.markdown(
        f"""
        <span class="tradehub-badge {status_class}">
            {text}
        </span>
        """,
        unsafe_allow_html=True
    )


def page_note(title, body):
    st.markdown(
        f"""
        <div class="page-note">
            <div class="page-note-title">{title}</div>
            <div class="page-note-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def table_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="table-header">
            <div>
                <div class="table-title">{title}</div>
                <div class="table-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
