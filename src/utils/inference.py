import argparse
import pandas as pd
import joblib
from feature_engineer import generate_features

def main(data_path, model_path, scaler_path, output_path=None):
    # Load new raw data for prediction
    df = pd.read_csv(data_path)

    # Generate features (no labels needed here)
    features, _ = generate_features(df)  # labels ignored during inference

    # Load scaler and model
    scaler = joblib.load(scaler_path)
    model = joblib.load(model_path)

    # Scale features
    features_scaled = scaler.transform(features)

    # Predict probabilities or labels
    predictions = model.predict(features_scaled)
    prediction_proba = model.predict_proba(features_scaled)[:, 1]  # Probability of class '1'

    # Add predictions to original dataframe (align on index)
    results = df.loc[features.index].copy()
    results['predicted_label'] = predictions
    results['predicted_probability'] = prediction_proba

    # Output results
    if output_path:
        results.to_csv(output_path, index=False)
        print(f"Saved prediction results to {output_path}")
    else:
        print(results[['close', 'predicted_label', 'predicted_probability']].head(20))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run inference on crypto price data")
    parser.add_argument("--data_path", type=str, required=True, help="CSV file path for new data")
    parser.add_argument("--model_path", type=str, default="models/trading_model.pkl", help="Path to saved model")
    parser.add_argument("--scaler_path", type=str, default="models/scaler.pkl", help="Path to saved scaler")
    parser.add_argument("--output_path", type=str, default=None, help="CSV path to save prediction results")

    args = parser.parse_args()
    main(args.data_path, args.model_path, args.scaler_path, args.output_path)
