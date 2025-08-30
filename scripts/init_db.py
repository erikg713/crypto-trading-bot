import sqlite3
from pathlib import Path

# ---------------------------
# CONFIGURATION
# ---------------------------
DB_PATH = Path("data/db/trader.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------
# INITIALIZATION
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------------------------
    # Table: market_data
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        interval TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,
        UNIQUE(symbol, interval, timestamp)
    )
    """)

    # ---------------------------
    # Table: trades
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        price REAL,
        size REAL,
        pnl REAL
    )
    """)

    # ---------------------------
    # Table: strategies
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS strategies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        params TEXT
    )
    """)

    # ---------------------------
    # Table: positions
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        entry_price REAL,
        size REAL,
        open_time DATETIME,
        close_price REAL,
        close_time DATETIME,
        pnl REAL
    )
    """)

    conn.commit()
    conn.close()
    print(f"[INFO] Database initialized at {DB_PATH}")

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    init_db()
