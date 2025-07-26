from sklearn.ensemble import RandomForestClassifier
import joblib
from src.collectors.fetch_historical import fetch_ohlcv
from src.features.feature_engineer import generate_features
from src.collectors.fetch_historical import fetch_ohlcv
from src.features.feature_engineer import generate_features
from sklearn.ensemble import RandomForestClassifier
import joblib
def train():
    df = fetch_ohlcv("BTCUSDT", "15m")
    X, y = generate_features(df)
    model = LGBMClassifier()
    model.fit(X[:-1000], y[:-1000])
    joblib.dump(model, 'models/signal_model.pkl')
def train_model():
    df = fetch_ohlcv()
    X, y = generate_features(df)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, "models/signal_model.pkl")
    print("✅ Model trained and saved.")

if __name__ == "__main__":
    train_model()

def train():
    df = fetch_ohlcv("BTCUSDT")
    X, y = generate_features(df)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)

    joblib.dump(clf, 'models/signal_model.pkl')
    print("Model trained and saved!")

if __name__ == "__main__":
    train()

