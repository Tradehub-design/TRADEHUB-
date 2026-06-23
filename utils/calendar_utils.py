import pandas as pd


def daily_trade_summary(df):
    if df.empty:
        return pd.DataFrame()

    daily = (
        df.groupby(df["trade_date"].dt.date)
        .agg(
            pnl=("net_profit", "sum"),
            trades=("ticket", "count"),
        )
        .reset_index()
    )

    daily = daily.rename(columns={"trade_date": "trade_date"})

    return daily
