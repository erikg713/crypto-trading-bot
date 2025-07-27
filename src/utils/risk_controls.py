MAX_TRADE_USDT = 1000
MAX_DAILY_TRADES = 20
trade_count = 0

def reset_counters():
    global trade_count
    trade_count = 0

def validate_risk(available_usdt, trade_amount):
    global trade_count
    if trade_count >= MAX_DAILY_TRADES:
        print("Daily trade limit reached")
        return False
    if trade_amount > available_usdt:
        print("Not enough balance")
        return False
    if trade_amount > MAX_TRADE_USDT:
        print(f"Trade amount capped to {MAX_TRADE_USDT}")
        trade_amount = MAX_TRADE_USDT
    trade_count += 1
    return True

