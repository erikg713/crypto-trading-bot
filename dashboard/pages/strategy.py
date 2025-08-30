from dash import html, dcc
from dashboard.components import strategy_controls_component

def strategy_layout(symbol="ETHUSDT"):
    """
    Strategy page layout for adjusting trading strategy parameters dynamically.
    """
    layout = html.Div([
        html.H2(f"{symbol} Strategy Controls"),
        html.P("Adjust your strategy parameters below:"),
        
        # Strategy Controls component (sliders, inputs)
        strategy_controls_component(default_short=10, default_long=50),

        html.Div(id="strategy-output", style={"marginTop": "20px", "padding": "10px", "border": "1px solid #ccc", "border-radius": "5px"})
    ], style={"padding": "20px"})
    
    return layout
