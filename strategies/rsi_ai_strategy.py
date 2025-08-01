# strategies/rsi_ai_strategy.py
import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from sklearn.linear_model import LogisticRegression

class RSIAIStrategy:
    def __init__(self, model=None):
        self.model = model or LogisticRegression()

    def train(self, df):
        df = self._add_features(df)
        X = df[['rsi', 'close', 'volume']].dropna()
        y = np.where(df['close'].shift(-1) > df['close'], 1, 0)  # 1 = price goes up
        self.model.fit(X, y)

    def _add_features(self, df):
        rsi = RSIIndicator(close=df['close'], window=14)
        df['rsi'] = rsi.rsi()
        return df

    def decide(self, df):
        df = self._add_features(df.copy())
        latest = df.iloc[-1]
        X_pred = np.array([[latest['rsi'], latest['close'], latest['volume']]])
        ai_prediction = self.model.predict(X_pred)[0]

        if latest['rsi'] < 30 and ai_prediction == 1:
            return 'BUY'
        elif latest['rsi'] > 70 and ai_prediction == 0:
            return 'SELL'
        else:
            return 'HOLD'