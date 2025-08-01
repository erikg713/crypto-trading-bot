# main.py
import argparse
from strategies.rsi_strategy import RSIStrategy
from visuals.backtest_plot import plot_rsi_strategy

...

if args.strategy == 'rsi':
    strategy = RSIStrategy()
    df = fetch_historical_data(args.exchange)
    df_signals = strategy.generate_signals(df)

    if args.backtest:
        plot_rsi_strategy(df_signals)
from core.trader import Trader
elif args.strategy == 'hybrid_rsi_ai':
    from strategies.hybrid_rsi_ai_strategy import HybridRSIAIStrategy
    strategy = HybridRSIAIStrategy()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exchange", type=str, required=True)
    parser.add_argument("--strategy", type=str, required=True)
    args = parser.parse_args()

    trader = Trader(exchange_name=args.exchange, strategy_name=args.strategy)
    trader.run()
