import plotly.graph_objects as go

def plot_indicators(fig, df, indicators=["sma_10", "sma_50", "rsi"]):
    """
    Overlay indicators on an existing candlestick figure.
    df: DataFrame containing indicator columns
    indicators: list of column names to plot
    """
    for ind in indicators:
        if ind in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[ind],
                mode='lines',
                name=ind
            ))
    return fig
