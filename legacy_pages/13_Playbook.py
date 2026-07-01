import streamlit as st

from core.ui import load_css, app_header, section
from core.components import command_card, feature_card, stat_row
from utils.supabase_client import get_supabase_client
from core.playbook_engine import PlaybookEngine


load_css()

app_header(
    "📚 Playbook",
    "Build and maintain your trading strategy library."
)

supabase = get_supabase_client()

section("Create Playbook")

with st.form("create_playbook_form"):
    name = st.text_input(
        "Playbook Name",
        placeholder="Example: A+ London Liquidity Sweep"
    )

    description = st.text_area(
        "Description",
        placeholder="Describe when this setup should be used."
    )

    col1, col2 = st.columns(2)

    with col1:
        market = st.selectbox(
            "Market",
            ["Forex", "Gold", "Crypto", "Indices", "Stocks", "Other"]
        )

        timeframe = st.selectbox(
            "Primary Timeframe",
            ["1M", "5M", "15M", "30M", "1H", "4H", "1D", "1W"]
        )

    with col2:
        ideal_session = st.selectbox(
            "Ideal Session",
            ["Asia", "London", "New York", "Any"]
        )

        risk_percent = st.number_input(
            "Risk %",
            min_value=0.0,
            max_value=10.0,
            value=0.5,
            step=0.1
        )

    target_rr = st.number_input(
        "Target R:R",
        min_value=0.0,
        max_value=20.0,
        value=2.0,
        step=0.1
    )

    submitted = st.form_submit_button("Create Playbook")

    if submitted:
        if not name:
            st.error("Playbook name is required.")
        else:
            payload = PlaybookEngine.create_playbook_payload(
                name,
                description,
                market,
                timeframe,
                ideal_session,
                risk_percent,
                target_rr
            )

            supabase.table("playbooks").insert(payload).execute()

            st.success("Playbook created.")
            st.cache_data.clear()
            st.rerun()

section("Existing Playbooks")

playbook_response = (
    supabase.table("playbooks")
    .select("*")
    .order("created_at", desc=True)
    .execute()
)

playbooks = playbook_response.data or []

if not playbooks:
    command_card(
        "No playbooks yet",
        "Create your first strategy playbook above.",
        "Example: A+ London Sweep."
    )
    st.stop()

for playbook in playbooks:
    feature_card(
        playbook.get("name"),
        playbook.get("description") or "No description added.",
        playbook.get("market") or "Playbook"
    )

    stat_row([
        {
            "label": "Timeframe",
            "value": playbook.get("timeframe") or "-",
            "helper": "Primary timeframe",
            "status": "neutral",
        },
        {
            "label": "Session",
            "value": playbook.get("ideal_session") or "-",
            "helper": "Ideal trading window",
            "status": "neutral",
        },
        {
            "label": "Target RR",
            "value": playbook.get("target_rr") or 0,
            "helper": "Expected reward",
            "status": "positive",
        },
    ])

    with st.expander("Rules"):
        with st.form(f"rule_form_{playbook['id']}"):
            rule_text = st.text_input(
                "Rule",
                placeholder="Example: Must sweep previous high/low"
            )

            rule_type = st.selectbox(
                "Rule Type",
                [
                    "Entry",
                    "Exit",
                    "Risk",
                    "Session",
                    "Psychology",
                    "Confirmation",
                    "Other",
                ]
            )

            is_required = st.checkbox(
                "Required Rule",
                value=True
            )

            rule_submitted = st.form_submit_button("Add Rule")

            if rule_submitted:
                if not rule_text:
                    st.error("Rule text is required.")
                else:
                    rule_payload = PlaybookEngine.create_rule_payload(
                        playbook["id"],
                        rule_text,
                        rule_type,
                        is_required
                    )

                    supabase.table("playbook_rules").insert(rule_payload).execute()

                    st.success("Rule added.")
                    st.cache_data.clear()
                    st.rerun()

        rules_response = (
            supabase.table("playbook_rules")
            .select("*")
            .eq("playbook_id", playbook["id"])
            .execute()
        )

        rules = rules_response.data or []

        if rules:
            for rule in rules:
                required = "Required" if rule.get("is_required") else "Optional"
                st.markdown(
                    f"- **{rule.get('rule_type')}**: {rule.get('rule_text')} _({required})_"
                )
        else:
            st.info("No rules added yet.")
