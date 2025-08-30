from dash import dcc, html

def strategy_controls_component(default_short=10, default_long=50):
    """
    Returns UI components for adjusting strategy parameters.
    """
    controls = html.Div([
        html.H4("Strategy Controls"),
        html.Label("Short MA Window"),
        dcc.Slider(min=1, max=50, step=1, value=default_short, id="short-ma-slider"),
        html.Label("Long MA Window"),
        dcc.Slider(min=10, max=200, step=1, value=default_long, id="long-ma-slider")
    ], style={"padding": "10px", "border": "1px solid #ccc", "border-radius": "5px", "width": "300px"})
    return controls
