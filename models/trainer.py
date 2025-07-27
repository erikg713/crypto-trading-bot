# models/trainer.py

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Paths
DATA_PATH = "../data/training/features.csv"
MODEL_PATH = "../models/model.pkl"
MODEL_PATH = "../models/signal_model.pkl"

def load_data(path):
    """Load feature matrix and labels"""
    df = pd.read_csv(path)
    
    # Assume target is in a column named 'target'
    if 'target' not in df.columns:
        raise ValueError("Missing 'target' column in dataset.")
    
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def train_model(X, y):
    """Train a classification model"""
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    print("✅ Model trained")
    print("📊 Validation Accuracy:", accuracy_score(y_val, y_pred))
    print("\n📈 Classification Report:\n", classification_report(y_val, y_pred))

    return model

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"💾 Model saved to {path}")

def main():
    print("🚀 Starting training pipeline...")
    X, y = load_data(DATA_PATH)
    model = train_model(X, y)
    save_model(model, MODEL_PATH)

if __name__ == "__main__":
    main()


# models/trainer.py

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Paths
DATA_PATH = "../data/training/features.csv"
MODEL_PATH = "../models/model.pkl"

def load_data(path):
    """Load feature matrix and labels"""
    df = pd.read_csv(path)
    
    # Assume target is in a column named 'target'
    if 'target' not in df.columns:
        raise ValueError("Missing 'target' column in dataset.")
    
    X = df.drop(columns=['target'])
    y = df['target']
    return X, y

def train_model(X, y):
    """Train a classification model"""
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_val)
    print("✅ Model trained")
    print("📊 Validation Accuracy:", accuracy_score(y_val, y_pred))
    print("\n📈 Classification Report:\n", classification_report(y_val, y_pred))

    return model

def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"💾 Model saved to {path}")

def main():
    print("🚀 Starting training pipeline...")
    X, y = load_data(DATA_PATH)
    model = train_model(X, y)
    save_model(model, MODEL_PATH)

if __name__ == "__main__":
    main()
