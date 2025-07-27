import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from src.data.training.feature_engineer import generate_features
from src.data.models.model_factory import get_model
from src.data.models.utils.save_model import save_model

def main():
    # 1. Load raw historical price data (update path as needed)
    df = pd.read_csv("data/historical_prices.csv")

    # 2. Generate features and labels
    features, labels = generate_features(df)

    # 3. Split into train/test (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # 4. Initialize model via factory
    model = get_model("random_forest")

    # 5. Train model
    model.train(X_train, y_train)

    # 6. Predict on test set
    y_pred = model.predict(X_test)

    # 7. Evaluate performance
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # 8. Save the trained model to disk with utility
    save_model(model.model, "model_v1.pkl")  # .model accesses underlying sklearn model

if __name__ == "__main__":
    main()
