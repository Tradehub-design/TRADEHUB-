import streamlit as st


class V2Style:

    @staticmethod
    def load():
        st.markdown(
            """
            <style>
            :root {
                --bg: #050b14;
                --panel: #0b1626;
                --panel2: #0f2137;
                --border: rgba(148, 163, 184, 0.18);
                --text: #f8fafc;
                --muted: #94a3b8;
                --green: #22c55e;
                --red: #ef4444;
                --blue: #3b82f6;
                --yellow: #facc15;
            }

            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at top left, rgba(59,130,246,.12), transparent 28%),
                    radial-gradient(circle at top right, rgba(34,197,94,.08), transparent 24%),
                    var(--bg);
                color: var(--text);
            }

            [data-testid="stSidebar"] {
                background: #06111f;
                border-right: 1px solid var(--border);
            }

            .block-container {
                max-width: 1600px;
                padding-top: 1rem;
                padding-bottom: 2rem;
            }

            .v2-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 18px;
            }

            .v2-title {
                font-size: 30px;
                font-weight: 900;
                letter-spacing: -0.04em;
            }

            .v2-subtitle {
                color: var(--muted);
                margin-top: 4px;
            }

            .v2-card {
                background: linear-gradient(180deg, #0d1a2b, #07111f);
                border: 1px solid var(--border);
                border-radius: 18px;
                padding: 18px;
                box-shadow: 0 18px 45px rgba(0,0,0,.26);
            }

            .v2-card-title {
                font-size: 13px;
                text-transform: uppercase;
                color: var(--muted);
                font-weight: 800;
                margin-bottom: 10px;
            }

            .v2-kpi-value {
                font-size: 28px;
                font-weight: 900;
            }

            .v2-muted {
                color: var(--muted);
                font-size: 13px;
            }

            .green { color: var(--green); }
            .red { color: var(--red); }
            .blue { color: var(--blue); }
            .yellow { color: var(--yellow); }

            .v2-section {
                font-size: 18px;
                font-weight: 900;
                margin: 24px 0 12px 0;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
