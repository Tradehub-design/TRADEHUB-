import streamlit as st


def show_funded_tracker(accounts, rules):
    st.subheader("💰 Funded Account Tracker")

    if not accounts:
        st.info("No accounts found.")
        return

    for account in accounts:
        account_number = account.get("account_number")
        account_name = account.get("account_name") or account_number
        current_balance = account.get("current_balance") or 0
        starting_balance = account.get("starting_balance") or 0

        rule = next(
            (r for r in rules if r.get("account_number") == account_number),
            None
        )

        with st.container(border=True):
            st.markdown(f"### {account_name}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Starting Balance", starting_balance)

            with col2:
                st.metric("Current Balance", current_balance)

            with col3:
                st.metric("Profit", round(current_balance - starting_balance, 2))

            if rule:
                st.write(f"**Daily Loss Limit:** {rule.get('max_daily_loss')}")
                st.write(f"**Max Total Loss:** {rule.get('max_total_loss')}")
                st.write(f"**Profit Target:** {rule.get('profit_target')}")
                st.write(f"**Minimum Trading Days:** {rule.get('min_trading_days')}")
