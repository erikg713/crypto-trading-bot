from rich.console import Console
from rich.table import Table
from src.learners.predict_signals import get_latest_signal

def show_live_status():
    console = Console()
    table = Table(title="Crypto Trading Bot Monitor")

    table.add_column("Metric", style="bold cyan")
    table.add_column("Value", style="bold green")

    signal, confidence = get_latest_signal()
    table.add_row("Signal", "BUY" if signal == 1 else "HOLD")
    table.add_row("Confidence", f"{confidence:.2f}")

    console.print(table)

if __name__ == "__main__":
    show_live_status()
