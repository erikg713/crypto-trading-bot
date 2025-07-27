# src/executors/risk_controls.py

"""
Risk management module to enforce daily trade caps, per-trade limits, and balance checks.
"""

from binance.exceptions import BinanceAPIException

# Constants
MAX_TRADE_USDT = 50.0         # Per-trade cap
MAX_DAILY_TRADES = 20         # Daily trade limit
MAX_DAILY_LOSS_USDT = 150.0   # Optional: Daily max drawdown

# Internal counters
trade_count = 0
daily_loss = 0.0

def reset_risk_counters():
    """
    Resets daily counters - should be triggered at UTC midnight by scheduler.
    """
    global trade_count, daily_loss
    trade_count = 0
    daily_loss = 0.0

def validate_risk(available_usdt: float, trade_amount: float, current_loss: float = 0.0) -> bool:
    """
    Validates whether a trade can be placed based on predefined risk rules.
    
    Args:
        available_usdt (float): Current USDT balance.
        trade_amount (float): USDT intended for trade.
        current_loss (float): Realized or unrealized loss to track drawdown.
    
    Returns:
        bool: True if trade is allowed, False otherwise.
    """
    global trade_count, daily_loss

    # Enforce daily trade count
    if trade_count >= MAX_DAILY_TRADES:
        print("❌ Daily trade count limit reached.")
        return False

    # Enforce balance availability
    if trade_amount > available_usdt:
        print("❌ Insufficient USDT balance.")
        return False

    # Enforce per-trade limit
    if trade_amount > MAX_TRADE_USDT:
        print(f"⚠️ Trade amount (${trade_amount}) exceeds max per trade limit (${MAX_TRADE_USDT}). Capping trade.")
        trade_amount = MAX_TRADE_USDT

    # Track loss (optional)
    daily_loss += current_loss
    if daily_loss >= MAX_DAILY_LOSS_USDT:
        print("🚫 Daily max loss threshold reached.")
        return False

    # Passed all checks
    trade_count += 1
    print(f"✅ Trade approved: ${trade_amount}. Trade count: {trade_count}/{MAX_DAILY_TRADES}")
    return True
