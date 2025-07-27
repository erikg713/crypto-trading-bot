import os
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_model(model, scaler, model_path, scaler_path):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    logging.info(f"Saved model to {model_path} and scaler to {scaler_path}")

def load_model(model_path, scaler_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    logging.info(f"Loaded model from {model_path} and scaler from {scaler_path}")
    return model, scaler

def train_model(X, y, test_size=0.2, random_state=42, model_cls=None, model_params=None):
    """
    Train a classifier model with scaling and train/test split.

    Args:
        X: Feature DataFrame or ndarray
        y: Labels Series or ndarray
        test_size: float, fraction for test split
        random_state: int for reproducibility
        model_cls: sklearn model class, e.g. RandomForestClassifier
        model_params: dict, model hyperparameters

    Returns:
        model: trained model
        scaler: fitted StandardScaler
        X_test_scaled, y_test: test data for evaluation
    """
    if model_cls is None:
        from sklearn.ensemble import RandomForestClassifier
        model_cls = RandomForestClassifier
    if model_params is None:
        model_params = {"n_estimators": 100, "random_state": random_state}

    logging.info("Splitting data into train and test sets")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logging.info("Scaling features")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logging.info(f"Training model: {model_cls.__name__} with params {model_params}")
    model = model_cls(**model_params)
    model.fit(X_train_scaled, y_train)

    logging.info("Evaluating model on test data")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    logging.info(f"Test Accuracy: {accuracy:.4f}")
    logging.info(f"Classification Report:\n{classification_report(y_test, y_pred)}")

    return model, scaler, X_test_scaled, y_test


