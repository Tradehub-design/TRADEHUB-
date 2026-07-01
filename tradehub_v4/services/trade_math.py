import pandas as pd


def prepare_trades(trades):
    if trades is None or trades.empty:
        return pd.DataFrame()
    df = trades.copy()
    if "trade_date" in df.columns:
        df["trade_date"] = pd.to_datetime(df["trade_date"], errors="coerce")
        df["date"] = df["trade_date"].dt.date
        df["weekday"] = df["trade_date"].dt.day_name()
        df["month"] = df["trade_date"].dt.strftime("%Y-%m")
        df["hour"] = df["trade_date"].dt.hour
    if "open_time" in df.columns:
        df["open_time_dt"] = pd.to_datetime(df["open_time"], errors="coerce")
        df["hold_minutes"] = (df["trade_date"] - df["open_time_dt"]).dt.total_seconds() / 60
    return df


def equity_curve(trades):
    df = prepare_trades(trades)
    if df.empty or "net_profit" not in df.columns or "trade_date" not in df.columns:
        return pd.DataFrame()
    df = df.dropna(subset=["trade_date"]).sort_values("trade_date").copy()
    df["equity_curve"] = df["net_profit"].cumsum()
    df["peak"] = df["equity_curve"].cummax()
    df["drawdown"] = df["equity_curve"] - df["peak"]
    return df


def group_summary(df, group_col):
    if df is None or df.empty or group_col not in df.columns or "net_profit" not in df.columns:
        return pd.DataFrame()
    result = (
        df.groupby(group_col)
        .agg(
            Trades=(group_col, "count"),
            NetProfit=("net_profit", "sum"),
            Average=("net_profit", "mean"),
            Wins=("net_profit", lambda x: (x > 0).sum()),
            Losses=("net_profit", lambda x: (x < 0).sum()),
        )
        .reset_index()
    )
    result["WinRate"] = (result["Wins"] / result["Trades"] * 100).round(1)
    result["NetProfit"] = result["NetProfit"].round(2)
    result["Average"] = result["Average"].round(2)
    return result.sort_values("NetProfit", ascending=False)


def daily_summary(df):
    df = prepare_trades(df)
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()
    result = (
        df.groupby("date")
        .agg(
            Trades=("date", "count"),
            NetProfit=("net_profit", "sum"),
            Wins=("net_profit", lambda x: (x > 0).sum()),
            Losses=("net_profit", lambda x: (x < 0).sum()),
        )
        .reset_index()
        .sort_values("date", ascending=False)
    )
    result["WinRate"] = (result["Wins"] / result["Trades"] * 100).round(1)
    result["NetProfit"] = result["NetProfit"].round(2)
    return result
