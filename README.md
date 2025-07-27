-------------------------------
#### crypto-trading-bot ####
-------------------------------

✅ Test Setup
Install testing tools:

bash
Copy
Edit
pip install pytest
Run the tests:

bash
Copy
Edit
pytest tests/
pip install pandas
pip install matplotlib
seaborn 
scikit-learn 
joblib


How to run?
Create a virtual env and install dependencies:

bash
Copy
Edit
pip install sqlalchemy binance alpaca_trade_api pandas
Set environment variables for API keys:

bash
Copy
Edit
export BINANCE_API_KEY=your_key
export BINANCE_API_SECRET=your_secret
export ALPACA_API_KEY=your_key
export ALPACA_SECRET_KEY=your_secret
Run the bot:

bash
Copy
Edit
python src/app.py
Summary
Minimal but fully runnable AI crypto trading bot example included.

Can extend to stocks & options by adding your own AI models and executors.

Modular and clean structure for expandability.

✅ How to Run
Ensure API keys are set for Binance and Alpaca.

pip install sqlalchemy binance alpaca_trade_api pandas

Run: python src/app.py

### TRAIN PIPELINE ###
```
python3 train_pipeline.py
---
```
python train_pipeline.py --data_path data/historical_prices.csv --model_dir models

--------------------------
## INFERENCE ##
----------------------
```
python inference.py --data_path data/new_prices.csv --output_path predictions.csv
```

---------------------------
## RUN DASHBOARD ##
--------------------------
```
streamlit run app.py
```


