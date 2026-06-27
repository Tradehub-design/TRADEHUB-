import streamlit as st


class TradeFilters:

    @staticmethod
    def render(df, key_prefix="trade"):
        symbols = ["All"]
        sessions = ["All"]

        if df is not None and not df.empty:
            if "symbol" in df.columns:
                symbols += sorted(df["symbol"].dropna().unique().tolist())

            if "session" in df.columns:
                sessions += sorted(df["session"].dropna().unique().tolist())

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            symbol = st.selectbox(
                "Symbol",
                symbols,
                key=f"{key_prefix}_symbol"
            )

        with col2:
            session = st.selectbox(
                "Session",
                sessions,
                key=f"{key_prefix}_session"
            )

        with col3:
            direction = st.selectbox(
                "Direction",
                ["All", "BUY", "SELL"],
                key=f"{key_prefix}_direction"
            )

        with col4:
            result = st.selectbox(
                "Result",
                ["All", "Win", "Loss", "Breakeven"],
                key=f"{key_prefix}_result"
            )

        search = st.text_input(
            "Search ticket or symbol",
            key=f"{key_prefix}_search"
        )

        return {
            "symbol": symbol,
            "session": session,
            "direction": direction,
            "result": result,
            "search": search,
        }

    @staticmethod
    def apply(df, filters):
        if df is None or df.empty:
            return df

        filtered = df.copy()

        if filters["symbol"] != "All" and "symbol" in filtered.columns:
            filtered = filtered[filtered["symbol"] == filters["symbol"]]

        if filters["session"] != "All" and "session" in filtered.columns:
            filtered = filtered[filtered["session"] == filters["session"]]

        if filters["direction"] != "All" and "direction" in filtered.columns:
            filtered = filtered[filtered["direction"] == filters["direction"]]

        if filters["result"] == "Win" and "net_profit" in filtered.columns:
            filtered = filtered[filtered["net_profit"] > 0]

        if filters["result"] == "Loss" and "net_profit" in filtered.columns:
            filtered = filtered[filtered["net_profit"] < 0]

        if filters["result"] == "Breakeven" and "net_profit" in filtered.columns:
            filtered = filtered[filtered["net_profit"] == 0]

        search = filters.get("search", "").strip().upper()

        if search:
            mask = False

            if "symbol" in filtered.columns:
                mask = filtered["symbol"].astype(str).str.upper().str.contains(search)

            if "ticket" in filtered.columns:
                ticket_mask = filtered["ticket"].astype(str).str.upper().str.contains(search)
                mask = mask | ticket_mask if hasattr(mask, "__iter__") else ticket_mask

            filtered = filtered[mask]

        return filtered
