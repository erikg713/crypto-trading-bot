import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib  # for saving model

from feature_engineer import generate_features

def load_data(path="data/historical_prices.csv") -> pd.DataFrame:
    return pd.read_csv(path)

def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Classification Report:\n", classification_report(y_test, preds))

def main():
    # Load raw data
    df = load_data()

    # Generate features and labels
    X, y = generate_features(df)

    # Train/test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train model
    model = train_model(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_test, y_test)

    # Save trained model to disk
    joblib.dump(model, "models/rf_model.joblib")
    print("Model saved to models/rf_model.joblib")

if __name__ == "__main__":
    main()
