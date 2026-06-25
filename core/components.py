import streamlit as st


def stat_row(items):
    cols = st.columns(len(items))

    for col, item in zip(cols, items):
        with col:
            label = item.get("label", "")
            value = item.get("value", "")
            helper = item.get("helper", "")
            status = item.get("status", "neutral")

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


def command_card(title, body, footer=""):
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
            <div class="metric-helper">{footer}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def feature_card(title, body, badge_text=""):
    badge_html = ""

    if badge_text:
        badge_html = f'<span class="badge">{badge_text}</span>'

    st.markdown(
        f"""
        <div class="metric-card">
            {badge_html}
            <div style="font-size:18px;font-weight:850;margin-top:8px;">{title}</div>
            <div style="color:#A4A8B7;font-size:14px;line-height:1.5;margin-top:8px;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def trade_quality_card(score, message):
    status = "positive" if score >= 75 else "negative" if score < 50 else "neutral"

    status_class = {
        "positive": "metric-positive",
        "negative": "metric-negative",
        "neutral": "metric-neutral",
    }[status]

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Trade Quality Score</div>
            <div class="metric-value {status_class}">{score}/100</div>
            <div class="metric-helper">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
