import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from feature_engineer import generate_features

@st.cache_resource
def load_model_and_scaler(model_path="models/trading_model.pkl", scaler_path="models/scaler.pkl"):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def predict(df, model, scaler):
    features, _ = generate_features(df)
    features_scaled = scaler.transform(features)
    predictions = model.predict(features_scaled)
    prediction_proba = model.predict_proba(features_scaled)[:, 1]
    results = df.loc[features.index].copy()
    results['Predicted Label'] = predictions
    results['Prediction Probability'] = prediction_proba
    return results

def plot_results(results):
    fig, ax1 = plt.subplots(figsize=(12,6))

    ax1.plot(results.index, results['close'], label='Close Price', color='blue')
    buy_signals = results[results['Predicted Label'] == 1]
    no_buy_signals = results[results['Predicted Label'] == 0]
    ax1.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', label='Buy Signal')
    ax1.scatter(no_buy_signals.index, no_buy_signals['close'], marker='v', color='red', label='No Buy Signal')

    ax2 = ax1.twinx()
    ax2.plot(results.index, results['Prediction Probability'], color='orange', alpha=0.6, label='Prediction Probability')
    ax2.set_ylabel('Probability')

    ax1.set_xlabel('Index')
    ax1.set_ylabel('Price')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title("Crypto Price and Prediction Signals")
    st.pyplot(fig)

def main():
    st.title("Crypto Price Prediction Dashboard")

    uploaded_file = st.file_uploader("Upload CSV with price data (must have 'close' column)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("Upload a CSV file to get started.")
        return

    model, scaler = load_model_and_scaler()

    with st.spinner("Generating predictions..."):
        results = predict(df, model, scaler)

    st.subheader("Prediction Results")
    st.dataframe(results[['close', 'Predicted Label', 'Prediction Probability']])

    plot_results(results)

if __name__ == "__main__":
    main()
    print("🚀 Initializing trading bot...")
    init_db()
    scheduler = JobScheduler()
    scheduler.add_job(trading_job, every=15, unit='minutes', job_name='Multi-Asset Trading Job')
    scheduler.run_forever()
