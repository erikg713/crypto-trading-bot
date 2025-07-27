# src/data/training/train_model.py

import joblib
from sklearn.ensemble import RandomForestClassifier
from src.data.training.prepare_dataset import prepare_dataset

def train_model(df, label_col='close', model_path='model.pkl'):
    """
    Train a RandomForest classifier on financial data.
    """
    X, y = prepare_dataset(df, label_col)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, model_path)
    print(f"✅ Model saved to {model_path}")

    return model
