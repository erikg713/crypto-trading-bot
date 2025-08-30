import dash
from dash import html

def portfolio_summary_component(equity: float = 0.0, pnl: float = 0.0):
    """
    Returns a summary card with portfolio stats.
    """
    card = html.Div([
        html.H4("Portfolio Summary"),
        html.P(f"Equity: ${equity:,.2f}"),
        html.P(f"PnL: ${pnl:,.2f}")
    ], style={"border": "1px solid #ccc", "padding": "10px", "border-radius": "5px", "width": "250px"})
    return card
