# 🤖 AI-CryptoTrader

An AI-powered trading bot that automates crypto (and future stock/option) strategies with real-time data analysis, multi-exchange support, and a modular design for seamless expansion.

---

## ✨ Features

- ✅ Multi-exchange support (Binance, Alpaca — extendable)  
- 📈 Real-time market data streaming and analysis  
- 🧠 AI / Custom strategy plug-ins (e.g., Moving Average Crossover, RSI, Reinforcement Learning)  
- 🧾 Automated order execution  
- 🛡️ Risk management (Stop-loss, Take-profit, Trailing Stop)  
- ⚙️ Modular codebase – plug in new assets, strategies, and exchanges  
- 🔧 Backtesting engine (Coming soon)  
- 📊 Live performance dashboard (Optional GUI or CLI-based)  

---

## 🛒 Trading Logic

**BUY if:**  
- AI model predicts upward trend with high confidence  
- AND RSI < 40 (supportive oversold condition)  

**SELL if:**  
- AI model predicts downward trend  
- OR RSI > 70 (overbought)  

**HOLD otherwise**

---

## 📂 Directory Structure
```
ai-crypto-trader/ ├── exchanges/ │   ├── binance.py │   ├── alpaca.py │   └── base_exchange.py ├── strategies/ │   ├── moving_average.py │   ├── rsi_strategy.py │   └── base_strategy.py ├── risk/ │   └── risk_manager.py ├── core/ │   ├── trader.py │   ├── data_streamer.py │   └── order_executor.py ├── config/ │   └── settings.yaml ├── logs/ │   └── trade_log.txt ├── main.py └── README.md
```
---

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/your-username/ai-crypto-trader.git
cd ai-crypto-trader

2. Install dependencies



pip install -r requirements.txt

3. Configure exchange keys



# config/settings.yaml
binance:
  api_key: "YOUR_BINANCE_KEY"
  api_secret: "YOUR_BINANCE_SECRET"

alpaca:
  api_key: "YOUR_ALPACA_KEY"
  api_secret: "YOUR_ALPACA_SECRET"

4. Run the bot



python main.py --exchange binance --strategy moving_average


---

🧠 Strategy System

Strategies are pluggable via the strategies/ module. Example:

class MovingAverageStrategy(BaseStrategy):
    def generate_signal(self, data):
        short_ma = data['close'].rolling(window=5).mean()
        long_ma = data['close'].rolling(window=20).mean()
        if short_ma[-1] > long_ma[-1]:
            return "BUY"
        elif short_ma[-1] < long_ma[-1]:
            return "SELL"
        return "HOLD"


---

🛡️ Risk Management Example

class RiskManager:
    def apply(self, position, price):
        if position.pnl_percent <= -5:
            return "CLOSE"
        elif position.pnl_percent >= 10:
            return "TAKE_PROFIT"
        return None

Run with backtesting:

python main.py --exchange binance --strategy moving_average --backtest


---

✅ RSI-based Strategy

Computes the Relative Strength Index (RSI) over a 14-period window.

BUY: RSI < 30 (oversold)

SELL: RSI > 70 (overbought)

HOLD: otherwise



---

📊 Roadmap

[x] Binance support

[x] Alpaca support

[x] Strategy plugin system

[x] Order execution

[ ] Live backtesting

[ ] Performance dashboard

[ ] Options trading support



---

📄 License

MIT License. Use at your own risk. Crypto trading involves significant risk.


---

🤝 Contributions

Contributions welcome! Fork the repo and submit a PR.

---
