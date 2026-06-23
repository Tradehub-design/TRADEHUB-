import streamlit as st


def show_funded_tracker(accounts, rules):

    st.subheader("💰 Funded Accounts")

    if not accounts:
        st.info("No accounts found.")
        return

    for account in accounts:

        rule = next(
            (
                r
                for r in rules
                if r["account_number"]
                == account["account_number"]
            ),
            None
        )

        with st.container(border=True):

            st.markdown(
                f"### {account.get('account_name')}"
            )

            st.write(
                f"Balance: {account.get('current_balance')}"
            )

            if rule:

                st.write(
                    f"Daily Loss: {rule.get('max_daily_loss')}"
                )

                st.write(
                    f"Max Loss: {rule.get('max_total_loss')}"
                )

                st.write(
                    f"Target: {rule.get('profit_target')}"
                )
