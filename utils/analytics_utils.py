import pandas as pd


def prepare_trades_dataframe(data):
    df = pd.DataFrame(data)

    if df.empty:
        return df

    if "trade_date" in df.columns:
        df["trade_date"] = pd.to_datetime(df["trade_date"])

    if "net_profit" in df.columns:
        df["net_profit"] = pd.to_numeric(df["net_profit"], errors="coerce").fillna(0)

    return df


def summary_stats(df):
    if df.empty:
        return {
            "total_trades": 0,
            "net_profit": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
        }

    total = len(df)
    wins = len(df[df["net_profit"] > 0])
    losses = len(df[df["net_profit"] < 0])
    net = df["net_profit"].sum()

    return {
        "total_trades": total,
        "net_profit": round(net, 2),
        "wins": wins,
        "losses": losses,
        "win_rate": round((wins / total) * 100, 2) if total else 0,
    }
