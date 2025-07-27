# src/data/training/evaluate_model.py

from sklearn.metrics import accuracy_score, classification_report

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model on test data.
    """
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)

    print(f"📊 Accuracy: {accuracy:.4f}")
    print("📄 Classification Report:")
    print(report)

    return accuracy, report
