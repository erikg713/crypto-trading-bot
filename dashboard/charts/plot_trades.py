import plotly.graph_objects as go

def overlay_trades(fig, trades_df):
    """
    Overlay buy/sell trades on existing figure.
    trades_df: columns ["timestamp", "side", "price"]
    """
    for _, row in trades_df.iterrows():
        color = "green" if row["side"].upper() == "BUY" else "red"
        fig.add_trace(go.Scatter(
            x=[row["timestamp"]],
            y=[row["price"]],
            mode="markers",
            marker=dict(color=color, size=10, symbol="triangle-up" if row["side"].upper()=="BUY" else "triangle-down"),
            name=f"{row['side']} Trade"
        ))
    return fig
