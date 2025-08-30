import dash
from dash import dash_table
import pandas as pd

def trade_table_component(trades_df: pd.DataFrame):
    """
    Returns a Dash DataTable showing executed trades.
    """
    if trades_df.empty:
        trades_df = pd.DataFrame(columns=["timestamp", "symbol", "side", "price", "size", "pnl"])
    
    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in trades_df.columns],
        data=trades_df.to_dict("records"),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px'},
        style_header={'fontWeight': 'bold'},
        page_size=10
    )
    return table
