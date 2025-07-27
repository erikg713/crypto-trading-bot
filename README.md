crypto-trading-bot — README.md

----------------------------
🚀 Project Overview
----------------------------
AI-powered crypto trading bot that automates trading strategies.

Supports multiple exchanges (Binance, Alpaca).

Features:

Real-time market data fetching.

Automated order execution.

Risk management with stop-loss and take-profit.

Customizable strategy implementation.


Modular, clean codebase designed for easy expansion to stocks/options.


⚙️ Features

Multi-exchange support.

Real-time data analysis.

Order execution automation.

Risk management tools.

Custom strategy support.



---

🛠️ Installation & Setup

1. Clone repo:

git clone https://github.com/erikg713/crypto-trading-bot.git
cd crypto-trading-bot


2. Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


4. Additional required packages for API and data handling:

pip install sqlalchemy binance alpaca_trade_api pandas matplotlib seaborn scikit-learn joblib


5. Set environment variables for API keys (example for Linux/macOS):

export BINANCE_API_KEY=your_key
export BINANCE_API_SECRET=your_secret
export ALPACA_API_KEY=your_key
export ALPACA_SECRET_KEY=your_secret




---

▶️ How to Run

Run the main trading bot:

python src/app.py

Run training pipeline on historical data:

python train_pipeline.py --data_path data/historical_prices.csv --model_dir models

Run inference/prediction on new data:

python inference.py --data_path data/new_prices.csv --output_path predictions.csv

Launch dashboard (Streamlit):

streamlit run app.py



---

✅ Testing

Install pytest for running tests:

pip install pytest

Run tests:

pytest tests/



---

📄 License

Licensed under MIT License.



---

If you want, I can help you:

Set up this bot on your machine,

Explain or customize any part of the code,

Help with adding new strategies or integrating other exchanges,

Or build related utilities like dashboard or training modules.


Just let me know!

