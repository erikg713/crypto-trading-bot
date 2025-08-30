from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

TRADES_FILE = Path("data/backtest/trades.csv")

# ---------------------------
# Helper Functions
# ---------------------------
def load_trades():
    if TRADES_FILE.exists():
        df = pd.read_csv(TRADES_FILE, parse_dates=["timestamp"])
        return df
    return pd.DataFrame(columns=["timestamp", "symbol", "side", "price", "size", "pnl"])

def compute_equity_curve(trades_df, starting_equity=10000):
    """
    Compute cumulative equity curve from trades.
    """
    if trades_df.empty:
        return pd.DataFrame({"timestamp": [], "equity": []})
    
    trades_df = trades_df.sort_values("timestamp")
    trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum()
    trades_df["equity"] = starting_equity + trades_df["cumulative_pnl"]
    return trades_df[["timestamp", "equity"]]

def compute_drawdown(equity_curve):
    """
    Compute drawdown series from equity curve.
    """
    if equity_curve.empty:
        return pd.DataFrame({"timestamp": [], "drawdown": []})
    
    equity_curve["rolling_max"] = equity_curve["equity"].cummax()
    equity_curve["drawdown"] = equity_curve["equity"] - equity_curve["rolling_max"]
    return equity_curve[["timestamp", "drawdown"]]

def compute_win_rate(trades_df):
    if trades_df.empty:
        return 0.0
    wins = trades_df[trades_df["pnl"] > 0].shape[0]
    total = trades_df.shape[0]
    return wins / total * 100

# ---------------------------
# Layout Function
# ---------------------------
def performance_layout(symbol="ETHUSDT"):
    trades = load_trades()
    trades_symbol = trades[trades["symbol"] == symbol]

    # Equity Curve
    equity_curve = compute_equity_curve(trades_symbol)
    equity_fig = go.Figure()
    equity_fig.add_trace(go.Scatter(
        x=equity_curve["timestamp"], y=equity_curve["equity"], mode="lines", name="Equity"
    ))
    equity_fig.update_layout(title=f"{symbol} Equity Curve", xaxis_title="Time", yaxis_title="Equity ($)")

    # Drawdown
    drawdown_curve = compute_drawdown(equity_curve)
    drawdown_fig = go.Figure()
    drawdown_fig.add_trace(go.Scatter(
        x=drawdown_curve["timestamp"], y=drawdown_curve["drawdown"], mode="lines", name="Drawdown"
    ))
    drawdown_fig.update_layout(title=f"{symbol} Drawdown", xaxis_title="Time", yaxis_title="Drawdown ($)")

    # Win Rate & Summary
    win_rate = compute_win_rate(trades_symbol)
    pnl_total = trades_symbol["pnl"].sum() if not trades_symbol.empty else 0
    summary_card = html.Div([
        html.H4("Performance Summary"),
        html.P(f"Total Trades: {trades_symbol.shape[0]}"),
        html.P(f"Total PnL: ${pnl_total:,.2f}"),
        html.P(f"Win Rate: {win_rate:.2f}%")
    ], style={"border": "1px solid #ccc", "padding": "10px", "border-radius": "5px", "width": "250px", "marginBottom": "20px"})

    layout = html.Div([
        html.H2(f"{symbol} Performance"),
        summary_card,
        dcc.Graph(figure=equity_fig),
        dcc.Graph(figure=drawdown_fig)
    ], style={"padding": "20px"})

    return layout
