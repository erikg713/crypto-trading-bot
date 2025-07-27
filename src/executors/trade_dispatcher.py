# src/executors/trade_dispatcher.py
def dispatch_trade(asset_type, asset_symbol, action, quantity):
    if asset_type == "crypto":
        if "pi" in asset_symbol.lower():
            from src.wallets.pi_wallet import send_pi_transaction
            return send_pi_transaction(...)
        else:
            from src.executors.crypto_executor import execute_crypto_trade
            return execute_crypto_trade(asset_symbol, action, quantity)
    elif asset_type == "stock":
        from src.executors.stock_executor import execute_stock_trade
        return execute_stock_trade(asset_symbol, quantity, action)
