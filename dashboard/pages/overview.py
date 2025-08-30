from dash import html, dcc
from dashboard.charts import plot_candlestick, overlay_trades, plot_indicators
from dashboard.components import portfolio_summary_component, strategy_controls_component, trade_table_component
import pandas as pd
from pathlib import Path

RAW_DATA_DIR = Path("data/raw/market")
TRADES_FILE = Path("data/backtest/trades.csv")

def load_data(symbol, interval="1h"):
    file_path = RAW_DATA_DIR / f"{symbol}_{interval}.csv"
    df = pd.read_csv(file_path, parse_dates=["open_time"])
    df.rename(columns={"open_time": "timestamp"}, inplace=True)
    return df

def load_trades():
    if TRADES_FILE.exists():
        return pd.read_csv(TRADES_FILE, parse_dates=["timestamp"])
    return pd.DataFrame(columns=["timestamp", "symbol", "side", "price", "size", "pnl"])

def overview_layout(symbol="ETHUSDT"):
    df = load_data(symbol)
    trades = load_trades()

    fig = plot_candlestick(df, title=f"{symbol} Candlestick Chart")
    fig = overlay_trades(fig, trades[trades["symbol"]==symbol])
    indicators = [col for col in df.columns if col.startswith("sma") or col.startswith("rsi")]
    fig = plot_indicators(fig, df, indicators)

    equity = 10000 + trades["pnl"].sum() if not trades.empty else 10000
    pnl = trades["pnl"].sum() if not trades.empty else 0

    layout = html.Div([
        html.H2(f"{symbol} Overview"),
        strategy_controls_component(),
        dcc.Graph(figure=fig),
        html.Div([
            portfolio_summary_component(equity, pnl),
            trade_table_component(trades[trades["symbol"]==symbol])
        ], style={"display": "flex", "justify-content": "center"})
    ])
    return layout
