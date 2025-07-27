import argparse
import logging
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib
import argparse
import logging
import os
import pandas as pd
from src.features.feature_engineer import generate_features
from src.learners.model_utils import train_model, save_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main(data_path, model_dir):
    logging.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)

    logging.info("Generating features and labels")
    features, labels = generate_features(df)

    logging.info("Training model")
    model, scaler, _, _ = train_model(features, labels)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "trading_model.pkl")
    scaler_path = os.path.join(model_dir, "scaler.pkl")

    logging.info("Saving model and scaler")
    save_model(model, scaler, model_path, scaler_path)

    logging.info("Training pipeline complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Train crypto price prediction model")
    parser.add_argument("--data_path", type=str, default="data/historical_prices.csv")
    parser.add_argument("--model_dir", type=str, default="models")
    args = parser.parse_args()

    main(args.data_path, args.model_dir)

from feature_engineer import generate_features

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main(data_path, model_dir):
    logging.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)

    logging.info("Generating features and labels")
    features, labels = generate_features(df)

    logging.info("Splitting dataset into train and test")
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )

    logging.info("Scaling features")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logging.info("Training RandomForestClassifier")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    logging.info("Evaluating model")
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Test Accuracy: {acc:.4f}")
    logging.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "trading_model.pkl")
    scaler_path = os.path.join(model_dir, "scaler.pkl")

    logging.info(f"Saving model to {model_path}")
    joblib.dump(model, model_path)

    logging.info(f"Saving scaler to {scaler_path}")
    joblib.dump(scaler, scaler_path)

    logging.info("Training pipeline complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train crypto price prediction model")
    parser.add_argument(
        "--data_path", type=str, default="data/historical_prices.csv", help="CSV file path for raw data"
    )
    parser.add_argument(
        "--model_dir", type=str, default="models", help="Directory to save trained model and scaler"
    )
    args = parser.parse_args()

    main(args.data_path, args.model_dir)
