from sklearn.ensemble import RandomForestClassifier
from .base_model import BaseModel

class RandomForestWrapper(BaseModel):
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def save(self, path):
        import joblib
        joblib.dump(self.model, path)

    def load(self, path):
        import joblib
        self.model = joblib.load(path)

def get_model(model_name: str):
    if model_name == "random_forest":
        return RandomForestWrapper()
    else:
        raise ValueError(f"Unknown model: {model_name}")

