from src.main import trading_job
from src.utils.scheduler import JobScheduler
from src.db.db_utils import init_db
import pandas as pd
from feature_engineer import generate_features

def main():
    # Example: load your data here (CSV or API)
    df = pd.read_csv("data/historical_prices.csv")

    features, labels = generate_features(df)

    print("Features sample:")
    print(features.head())

    print("Labels sample:")
    print(labels.head())

if __name__ == "__main__":
    init_db()
    scheduler = JobScheduler()
    scheduler.add_job(trading_job, every=15, unit='minutes', job_name='Multi-Asset Trading Job')
    scheduler.run_forever()

