from sklearn.ensemble import RandomForestClassifier
import joblib
from src.collectors.fetch_historical import fetch_ohlcv
from src.features.feature_engineer import generate_features

def train():
    df = fetch_ohlcv("BTCUSDT")
    X, y = generate_features(df)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)

    joblib.dump(clf, 'models/signal_model.pkl')
    print("Model trained and saved!")

if __name__ == "__main__":
    train()

