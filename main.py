# main.py
import argparse
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
