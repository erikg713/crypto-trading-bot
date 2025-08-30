from dash import html
from dashboard.components import trade_table_component
import pandas as pd
from pathlib import Path

TRADES_FILE = Path("data/backtest/trades.csv")

def load_trades():
    """
    Load trades from CSV.
    """
    if TRADES_FILE.exists():
        df = pd.read_csv(TRADES_FILE, parse_dates=["timestamp"])
        return df
    return pd.DataFrame(columns=["timestamp", "symbol", "side", "price", "size", "pnl"])

def trades_layout(symbol="ETHUSDT"):
    """
    Trades page layout: shows a detailed trade table and statistics.
    """
    trades = load_trades()
    trades_symbol = trades[trades["symbol"] == symbol]

    # Compute summary stats
    total_trades = trades_symbol.shape[0]
    total_pnl = trades_symbol["pnl"].sum() if not trades_symbol.empty else 0
    win_rate = (trades_symbol["pnl"] > 0).sum() / total_trades * 100 if total_trades > 0 else 0

    summary_card = html.Div([
        html.H4("Trade Summary"),
        html.P(f"Total Trades: {total_trades}"),
        html.P(f"Total PnL: ${total_pnl:,.2f}"),
        html.P(f"Win Rate: {win_rate:.2f}%")
    ], style={"border": "1px solid #ccc", "padding": "10px", "border-radius": "5px", "width": "250px", "marginBottom": "20px"})

    layout = html.Div([
        html.H2(f"{symbol} Trade History"),
        summary_card,
        trade_table_component(trades_symbol)
    ], style={"padding": "20px"})
    
    return layout
