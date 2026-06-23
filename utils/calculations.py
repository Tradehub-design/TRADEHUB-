def calculate_net_profit(profit, commission=0, swap=0):
    return (profit or 0) + (commission or 0) + (swap or 0)


def calculate_win_rate(wins, total_trades):
    if not total_trades:
        return 0
    return round((wins / total_trades) * 100, 2)


def calculate_profit_factor(gross_profit, gross_loss):
    if not gross_loss:
        return 0
    return round(abs(gross_profit / gross_loss), 2)
