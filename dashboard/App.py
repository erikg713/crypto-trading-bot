import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from dashboard.charts import plot_candlestick, overlay_trades, plot_indicators

# ---------------------------
# CONFIG
# ---------------------------
RAW_DATA_DIR = Path("data/raw/market")
TRADES_FILE = Path("data/backtest/trades.csv")
SYMBOL = "ETHUSDT"
INTERVAL = "1h"

# ---------------------------
# LOAD DATA
# ---------------------------
def load_data(symbol=SYMBOL, interval=INTERVAL):
    file_path = RAW_DATA_DIR / f"{symbol}_{interval}.csv"
    df = pd.read_csv(file_path, parse_dates=["open_time"])
    df.rename(columns={"open_time": "timestamp"}, inplace=True)
    return df

def load_trades():
    if TRADES_FILE.exists():
        return pd.read_csv(TRADES_FILE, parse_dates=["timestamp"])
    return pd.DataFrame(columns=["timestamp", "side", "price"])

# ---------------------------
# DASH APP
# ---------------------------
app = dash.Dash(__name__)
app.title = "AI-CryptoTrader Dashboard"

app.layout = html.Div([
    html.H1("AI-CryptoTrader Dashboard", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="symbol-dropdown",
        options=[{"label": "ETH/USDT", "value": "ETHUSDT"},
                 {"label": "SOL/USDT", "value": "SOLUSDT"}],
        value=SYMBOL,
        clearable=False
    ),
    dcc.Graph(id="candlestick-graph"),
    dcc.Interval(id="interval-component", interval=60*1000, n_intervals=0)  # Update every 60 sec
])

# ---------------------------
# CALLBACKS
# ---------------------------
@app.callback(
    Output("candlestick-graph", "figure"),
    Input("symbol-dropdown", "value"),
    Input("interval-component", "n_intervals")
)
def update_graph(symbol, n):
    df = load_data(symbol)
    trades = load_trades()
    fig = plot_candlestick(df, title=f"{symbol} Candlestick Chart")
    fig = overlay_trades(fig, trades[trades["symbol"] == symbol])
    # Plot SMA/RSI if available
    indicators = [col for col in df.columns if col.startswith("sma") or col.startswith("rsi")]
    fig = plot_indicators(fig, df, indicators)
    return fig

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
