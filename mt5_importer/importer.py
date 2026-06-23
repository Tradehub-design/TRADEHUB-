import MetaTrader5 as mt5
from datetime import datetime, timedelta
from utils.supabase_client import get_supabase_client


def connect_mt5():
    if not mt5.initialize():
        raise RuntimeError(mt5.last_error())


def disconnect_mt5():
    mt5.shutdown()


def get_closed_trades(days_back=365):
    date_to = datetime.now()
    date_from = date_to - timedelta(days=days_back)

    deals = mt5.history_deals_get(date_from, date_to)

    if deals is None:
        return []

    return deals


def import_trades(account_number):

    connect_mt5()

    supabase = get_supabase_client()

    deals = get_closed_trades()

    imported = 0

    for deal in deals:

        if deal.entry != mt5.DEAL_ENTRY_OUT:
            continue

        trade = {
            "ticket": int(deal.ticket),
            "account_number": str(account_number),
            "symbol": deal.symbol,
            "volume": float(deal.volume),
            "exit_price": float(deal.price),
            "trade_date": datetime.fromtimestamp(deal.time).date().isoformat(),
            "net_profit": float(deal.profit),
        }

        supabase.table("trades").upsert(
            trade,
            on_conflict="ticket"
        ).execute()

        imported += 1

    disconnect_mt5()

    return imported
