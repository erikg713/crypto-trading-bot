import psycopg2
import pandas as pd
from contextlib import contextmanager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "trading_bot"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password")
}

@contextmanager
def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """
    Initializes required tables for OHLCV and predictions.
    """
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv (
            id SERIAL PRIMARY KEY,
            symbol TEXT NOT NULL,
            interval TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume FLOAT,
            UNIQUE(symbol, interval, timestamp)
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS model_predictions (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            symbol TEXT NOT NULL,
            prediction FLOAT,
            actual FLOAT,
            model_version TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        conn.commit()

def insert_ohlcv(symbol: str, interval: str, df: pd.DataFrame):
    """
    Insert OHLCV data into the database.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        for index, row in df.iterrows():
            try:
                cur.execute("""
                    INSERT INTO ohlcv (symbol, interval, timestamp, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (symbol, interval, timestamp) DO NOTHING;
                """, (
                    symbol,
                    interval,
                    index.to_pydatetime(),
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row["volume"]
                ))
            except Exception as e:
                print(f"[ERROR] Failed to insert OHLCV row: {e}")
        conn.commit()

def insert_prediction(symbol: str, timestamp: pd.Timestamp, prediction: float, actual: float, model_version: str = "v1"):
    """
    Store model prediction results in the database.
    """
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO model_predictions (timestamp, symbol, prediction, actual, model_version)
                VALUES (%s, %s, %s, %s, %s);
            """, (
                timestamp.to_pydatetime(),
                symbol,
                prediction,
                actual,
                model_version
            ))
            conn.commit()
        except Exception as e:
            print(f"[ERROR] Failed to insert prediction: {e}")

def fetch_latest_ohlcv(symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
    """
    Fetch latest OHLCV records from database.
    """
    with get_connection() as conn:
        query = f"""
            SELECT timestamp, open, high, low, close, volume
            FROM ohlcv
            WHERE symbol = %s AND interval = %s
            ORDER BY timestamp DESC
            LIMIT %s;
        """
        df = pd.read_sql(query, conn, params=(symbol, interval, limit))
        df.set_index("timestamp", inplace=True)
        df = df.sort_index()
        return df

def fetch_predictions(symbol: str, limit: int = 100) -> pd.DataFrame:
    """
    Fetch latest predictions for a given symbol.
    """
    with get_connection() as conn:
        query = """
            SELECT timestamp, prediction, actual, model_version
            FROM model_predictions
            WHERE symbol = %s
            ORDER BY timestamp DESC
            LIMIT %s;
        """
        df = pd.read_sql(query, conn, params=(symbol, limit))
        return df

