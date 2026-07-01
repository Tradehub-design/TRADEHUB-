import streamlit as st


def load_style():
    st.markdown(
        """
        <style>
        :root {
            --bg: #050b14;
            --panel: #0b1626;
            --panel2: #0f2137;
            --border: rgba(148,163,184,.18);
            --text: #f8fafc;
            --muted: #94a3b8;
            --green: #22c55e;
            --red: #ef4444;
            --blue: #3b82f6;
            --yellow: #facc15;
            --purple: #a855f7;
        }
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(37,99,235,.16), transparent 30%),
                radial-gradient(circle at top right, rgba(34,197,94,.10), transparent 28%),
                var(--bg);
            color: var(--text);
        }
        [data-testid="stSidebar"] {
            background: #06111f;
            border-right: 1px solid var(--border);
        }
        .block-container {
            max-width: 1720px;
            padding-top: 1.1rem;
            padding-bottom: 2rem;
        }
        .v4-topbar {
            display:flex;
            align-items:center;
            justify-content:space-between;
            margin-bottom:18px;
        }
        .v4-title {
            font-size: 34px;
            font-weight: 950;
            letter-spacing:-.04em;
            color: var(--text);
        }
        .v4-subtitle { color: var(--muted); margin-top:4px; }
        .v4-actions { display:flex; gap:8px; }
        .v4-action {
            background: #0f2137;
            border: 1px solid var(--border);
            color: #cbd5e1;
            border-radius: 11px;
            padding: 7px 11px;
            font-size: 13px;
        }
        .v4-card {
            background: linear-gradient(180deg, #0d1a2b, #07111f);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px;
            box-shadow: 0 18px 45px rgba(0,0,0,.25);
            min-height: 112px;
        }
        .v4-label {
            color: var(--muted);
            font-size: 12px;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing:.04em;
        }
        .v4-value {
            font-size: 28px;
            font-weight: 950;
            margin-top: 8px;
        }
        .v4-helper { font-size:13px; margin-top:8px; }
        .v4-section {
            font-size: 20px;
            font-weight: 900;
            margin: 24px 0 12px 0;
        }
        .v4-soft-card {
            background: rgba(15,33,55,.78);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .green, .positive { color: var(--green); }
        .red, .negative { color: var(--red); }
        .blue { color: var(--blue); }
        .yellow, .warning { color: var(--yellow); }
        .muted, .neutral { color: var(--muted); }
        div[data-testid="stMetric"] {
            background: rgba(15,33,55,.55);
            border: 1px solid rgba(148,163,184,.12);
            padding: 14px;
            border-radius: 16px;
        }
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] {
            background: rgba(15,33,55,.65);
            border-radius: 12px;
            padding: 8px 14px;
            border: 1px solid rgba(148,163,184,.12);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
