from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    asset = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    trade_type = Column(String)  # buy or sell
    price = Column(Float)
    quantity = Column(Float)
    profit = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    trade_type = Column(String)  # "buy" or "sell"
    price = Column(Float)
    quantity = Column(Float)
    profit = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Trade(symbol={self.symbol}, type={self.trade_type}, price={self.price}, qty={self.quantity})>"


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True, index=True)
    asset = Column(String, index=True)
    balance = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Wallet(asset={self.asset}, balance={self.balance})>"


class StrategyLog(Base):
    __tablename__ = 'strategy_logs'

    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<StrategyLog(strategy={self.strategy_name}, result={self.result})>"


class Signal(Base):
    __tablename__ = 'signals'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    signal_type = Column(String)  # "buy" or "sell"
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Signal(symbol={self.symbol}, signal={self.signal_type}, confidence={self.confidence})>"

