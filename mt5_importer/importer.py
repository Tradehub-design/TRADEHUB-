import MetaTrader5 as mt5
from datetime import datetime, timedelta
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def connect_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    return True


def shutdown_mt5():
    mt5.shutdown()


def get_closed_trades(days_back=365):
    date_to = datetime.now()
    date_from = date_to - timedelta(days=days_back)

    deals = mt5.history_deals_get(date_from, date_to)

    if deals is None:
        return []

    closed_trades = []

    for deal in deals:
        if deal.entry == mt5.DEAL_ENTRY_OUT:
            closed_trades.append(deal)

    return closed_trades


def format_trade(deal, account_number):
    trade_date = datetime.fromtimestamp(deal.time).date().isoformat()
    close_time = datetime.fromtimestamp(deal.time).isoformat()

    direction = "BUY" if deal.type == mt5.DEAL_TYPE_BUY else "SELL"

    profit = float(deal.profit or 0)
    commission = float(deal.commission or 0)
    swap = float(deal.swap or 0)

    return {
        "ticket": int(deal.ticket),
        "account_number": str(account_number),
        "symbol": deal.symbol,
        "direction": direction,
        "volume": float(deal.volume),
        "exit_price": float(deal.price),
        "close_time": close_time,
        "trade_date": trade_date,
        "profit": profit,
        "commission": commission,
        "swap": swap,
        "net_profit": profit + commission + swap,
    }


def import_trades(account_number, days_back=365):
    connect_mt5()

    deals = get_closed_trades(days_back)

    imported = 0

    for deal in deals:
        trade = format_trade(deal, account_number)

        supabase.table("trades").upsert(
            trade,
            on_conflict="ticket"
        ).execute()

        imported += 1

    shutdown_mt5()

    return imported


if __name__ == "__main__":
    ACCOUNT_NUMBER = "PUT_YOUR_MT5_ACCOUNT_NUMBER_HERE"

    total = import_trades(ACCOUNT_NUMBER)

    print(f"Imported {total} trades.")
