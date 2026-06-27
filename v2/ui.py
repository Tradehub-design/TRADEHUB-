import streamlit as st


class V2UI:

    @staticmethod
    def header(title, subtitle=""):
        st.markdown(
            f"""
            <div class="v2-header">
                <div>
                    <div class="v2-title">{title}</div>
                    <div class="v2-subtitle">{subtitle}</div>
                </div>
                <div class="v2-muted">⋯</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def section(title):
        st.markdown(
            f'<div class="v2-section">{title}</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def card(title, body, footer=""):
        st.markdown(
            f"""
            <div class="v2-card">
                <div class="v2-card-title">{title}</div>
                <div>{body}</div>
                <div class="v2-muted">{footer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def kpi(title, value, helper="", status="green"):
        st.markdown(
            f"""
            <div class="v2-card">
                <div class="v2-card-title">{title}</div>
                <div class="v2-kpi-value">{value}</div>
                <div class="{status}">{helper}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
