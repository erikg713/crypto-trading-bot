import logging
from sqlalchemy.orm import Session
from src.db.models import Wallet, Trade
from datetime import datetime

logger = logging.getLogger(__name__)

from src.executors.risk_controls import validate_risk

class PortfolioManager:
    # ... existing methods ...

    def execute_trade(self, symbol: str, trade_type: str, price: float, amount_usdt: float):
        available = self.get_balance('USDT')
        if not validate_risk(available, amount_usdt):
            return False

        # Calculate quantity from amount_usdt
        qty = amount_usdt / price

        # Deduct USDT, add asset to wallet
        self.update_balance('USDT', -amount_usdt)
        self.update_balance(symbol, qty)

        # Record the trade
        self.record_trade(symbol, trade_type, price, qty)
        return True


class PortfolioManager:
    def __init__(self, db: Session):
        self.db = db

    def get_balance(self, asset: str) -> float:
        wallet = self.db.query(Wallet).filter(Wallet.asset == asset.upper()).first()
        return wallet.balance if wallet else 0.0

    def update_balance(self, asset: str, amount: float, replace: bool = False):
        asset = asset.upper()
        wallet = self.db.query(Wallet).filter(Wallet.asset == asset).first()
        now = datetime.utcnow()

        if wallet:
            if replace:
                wallet.balance = amount
            else:
                wallet.balance += amount
            wallet.updated_at = now
            logger.info(f"Updated balance for {asset}: {wallet.balance}")
        else:
            wallet = Wallet(asset=asset, balance=amount, updated_at=now)
            self.db.add(wallet)
            logger.info(f"Created new wallet for {asset} with balance {amount}")
        self.db.commit()

    def get_portfolio(self):
        wallets = self.db.query(Wallet).all()
        return {wallet.asset: wallet.balance for wallet in wallets}

    def record_trade(self, symbol: str, trade_type: str, price: float, qty: float, profit: float = 0.0):
        trade = Trade(
            symbol=symbol.upper(),
            trade_type=trade_type.lower(),
            price=price,
            quantity=qty,
            profit=profit,
            timestamp=datetime.utcnow()
        )
        self.db.add(trade)
        self.db.commit()
        logger.info(f"Trade recorded: {trade_type.upper()} {qty} {symbol.upper()} at {price}")

    def calculate_total_value(self, prices: dict) -> float:
        """
        Calculate total value of the portfolio in quote currency (e.g., USDT)
        :param prices: dict of {asset: price_in_usdt}
        """
        total_value = 0.0
        for wallet in self.db.query(Wallet).all():
            asset = wallet.asset.upper()
            balance = wallet.balance
            price = prices.get(asset, 0)
            total_value += balance * price
        logger.info(f"Total portfolio value: {total_value}")
        return total_value

