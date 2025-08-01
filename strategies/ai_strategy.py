# strategies/ai_strategy.py
from strategies.base_strategy import BaseStrategy
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

class AIStrategy(BaseStrategy):
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(50))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model

    def train(self, prices, labels):
        X = np.array([prices[i-50:i] for i in range(50, len(prices))])
        X = X.reshape((X.shape[0], X.shape[1], 1))
        y = np.array(labels[50:])
        self.model.fit(X, y, epochs=10, batch_size=32)
        self.model.save("ai_model.h5")

    def generate_signal(self, data):
        prices = data['close'][-50:]
        X = np.array(prices).reshape((1, 50, 1))
        prediction = self.model.predict(X)[0][0]
        if prediction > 0.6:
            return "BUY"
        elif prediction < 0.4:
            return "SELL"
        else:
            return "HOLD"