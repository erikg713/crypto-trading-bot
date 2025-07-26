from src.learners.train_model import train_model
from src.learners.predict_signals import get_latest_signal

def test_model_training_and_prediction():
    train_model()
    signal, confidence = get_latest_signal()
    assert signal in [0, 1]
    assert 0 <= confidence <= 1

