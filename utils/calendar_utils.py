import pandas as pd


def daily_trade_summary(df):
    if df.empty:
        return pd.DataFrame()

    daily = (
        df.groupby(df["trade_date"].dt.date)
        .agg(
            net_profit=("net_profit", "sum"),
            total_trades=("ticket", "count"),
        )
        .reset_index()
    )

    return daily
