class ReportEngine:

    @staticmethod
    def daily(report):

        return f"""
Trades: {report['total_trades']}

Win Rate: {report['win_rate']}%

Net Profit: {report['net_profit']}

Best Symbol: {report['best_symbol']}

Best Session: {report['best_session']}
"""
