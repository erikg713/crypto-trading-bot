import joblib
from sklearn.metrics import accuracy_score, classification_report
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split

from src.collectors.fetch_historical import fetch_ohlcv
from src.features.feature_engineer import generate_features

def train():
    print("Fetching historical data...")
    df = fetch_ohlcv(symbol="BTCUSDT", interval="15m", limit=1000)

    print("Generating features...")
    X, y = generate_features(df)

    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    print("Training model...")
    model = LGBMClassifier(n_estimators=100, learning_rate=0.1)
    model.fit(X_train, y_train)

    print("Evaluating...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    print("Saving model...")
    joblib.dump(model, "models/signal_model.pkl")
    print("✅ Model saved.")

if __name__ == "__main__":
    train()