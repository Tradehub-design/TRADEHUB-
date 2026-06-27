import streamlit as st


class V2Style:

    @staticmethod
    def load():
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at top left, rgba(37,99,235,.16), transparent 30%),
                    radial-gradient(circle at top right, rgba(34,197,94,.08), transparent 28%),
                    #050b14;
                color: #f8fafc;
            }

            [data-testid="stSidebar"] {
                background: #06111f;
                border-right: 1px solid rgba(148,163,184,.18);
            }

            .block-container {
                max-width: 1650px;
                padding-top: 1rem;
                padding-bottom: 2rem;
            }

            .v2-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }

            .v2-title {
                font-size: 32px;
                font-weight: 900;
                letter-spacing: -0.04em;
            }

            .v2-subtitle {
                color: #94a3b8;
                margin-top: 4px;
            }

            .v2-card {
                background: linear-gradient(180deg, #0d1a2b, #07111f);
                border: 1px solid rgba(148,163,184,.18);
                border-radius: 18px;
                padding: 18px;
                box-shadow: 0 18px 45px rgba(0,0,0,.25);
                min-height: 112px;
            }

            .v2-label {
                color: #94a3b8;
                font-size: 12px;
                font-weight: 800;
                text-transform: uppercase;
            }

            .v2-value {
                font-size: 28px;
                font-weight: 900;
                margin-top: 8px;
            }

            .v2-section {
                font-size: 18px;
                font-weight: 900;
                margin: 22px 0 10px 0;
            }

            .green { color: #22c55e; }
            .red { color: #ef4444; }
            .blue { color: #3b82f6; }
            .yellow { color: #facc15; }
            .muted { color: #94a3b8; }

            .quick-actions {
                display: flex;
                gap: 8px;
                justify-content: flex-end;
            }

            .quick-action {
                background: #0f2137;
                border: 1px solid rgba(148,163,184,.2);
                border-radius: 10px;
                padding: 7px 11px;
                font-size: 13px;
                color: #cbd5e1;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
