class TradeDetailsEngine:

    @staticmethod
    def summary(trade):

        return {

            "pair": trade.get("symbol"),

            "direction": trade.get("direction"),

            "profit": trade.get("net_profit"),

            "entry": trade.get("entry_price"),

            "exit": trade.get("exit_price"),

            "lots": trade.get("volume"),

            "date": trade.get("trade_date")
        }
