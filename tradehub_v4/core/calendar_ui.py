import calendar
import pandas as pd
import streamlit as st


class CalendarUI:

    @staticmethod
    def month_selector(trades):
        df = trades.copy()
        df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")
        df = df.dropna(subset=["trade_date"])

        months = sorted(df["trade_date"].dt.strftime("%Y-%m").unique().tolist())

        if not months:
            return None

        return st.selectbox(
            "Month",
            months,
            index=len(months) - 1
        )

    @staticmethod
    def render_month(trades, selected_month):
        df = trades.copy()
        df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")
        df = df.dropna(subset=["trade_date"])
        df["date"] = df["trade_date"].dt.date
        df["month"] = df["trade_date"].dt.strftime("%Y-%m")

        month_df = df[df["month"] == selected_month]

        year, month = map(int, selected_month.split("-"))

        daily = (
            month_df.groupby("date")
            .agg(
                trades=("ticket", "count"),
                pnl=("net_profit", "sum"),
                wins=("net_profit", lambda x: (x > 0).sum()),
                losses=("net_profit", lambda x: (x < 0).sum()),
            )
            .reset_index()
        )

        daily_lookup = {
            row["date"]: row.to_dict()
            for _, row in daily.iterrows()
        }

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdatescalendar(year, month)

        st.markdown(
            """
            <style>
            .calendar-grid {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 10px;
            }

            .calendar-head {
                color: #94a3b8;
                font-size: 13px;
                font-weight: 800;
                text-align: center;
                padding: 8px;
            }

            .calendar-day {
                min-height: 115px;
                background: linear-gradient(180deg, #0d1a2b, #07111f);
                border: 1px solid rgba(148,163,184,.18);
                border-radius: 16px;
                padding: 12px;
            }

            .calendar-muted {
                opacity: .28;
            }

            .calendar-date {
                font-weight: 900;
                font-size: 16px;
            }

            .calendar-pnl-green {
                color: #22c55e;
                font-weight: 900;
                margin-top: 10px;
                font-size: 20px;
            }

            .calendar-pnl-red {
                color: #ef4444;
                font-weight: 900;
                margin-top: 10px;
                font-size: 20px;
            }

            .calendar-small {
                color: #94a3b8;
                font-size: 12px;
                margin-top: 6px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        html = "<div class='calendar-grid'>"

        for day_name in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            html += f"<div class='calendar-head'>{day_name}</div>"

        for week in weeks:
            for day in week:
                info = daily_lookup.get(day)
                muted = "calendar-muted" if day.month != month else ""

                if info:
                    pnl = round(info["pnl"], 2)
                    pnl_class = "calendar-pnl-green" if pnl >= 0 else "calendar-pnl-red"
                    pnl_text = f"+${pnl:,.2f}" if pnl >= 0 else f"-${abs(pnl):,.2f}"

                    body = f"""
                    <div class="calendar-date">{day.day}</div>
                    <div class="{pnl_class}">{pnl_text}</div>
                    <div class="calendar-small">{int(info["trades"])} trades</div>
                    <div class="calendar-small">{int(info["wins"])}W / {int(info["losses"])}L</div>
                    """
                else:
                    body = f"""
                    <div class="calendar-date">{day.day}</div>
                    <div class="calendar-small">No trades</div>
                    """

                html += f"<div class='calendar-day {muted}'>{body}</div>"

        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

        return month_df
