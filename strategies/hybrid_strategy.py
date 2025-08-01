import numpy as np
from .ai_strategy import AIStrategy
from .rsi_strategy import RSIIndicator

class HybridStrategy:
    def __init__(self):
        self.ai = AIStrategy()
        self.rsi = RSIIndicator()
        self.confidence_threshold = 0.6  # adjustable

    def train_ai(self, prices, labels):
        self.ai.train(prices, labels)

    def generate_signal(self, prices):
        if len(prices) < 15:
            return 'HOLD'

        rsi_value = self.rsi.calculate(prices)
        ai_prediction = self.ai.predict(prices)
        ai_confidence = ai_prediction[0]  # probability of upward movement

        # Hybrid Logic
        if ai_confidence > self.confidence_threshold and rsi_value < 40:
            return 'BUY'
        elif ai_confidence < 1 - self.confidence_threshold or rsi_value > 70:
            return 'SELL'
        return 'HOLD'