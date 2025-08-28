"""
logs/logger.py
==============

Utility for logging system events to `system_logs.txt`.
"""

import logging
from pathlib import Path

# Ensure the logs directory exists
LOG_DIR = Path(__file__).parent
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "system_logs.txt"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()  # optional: also print to console
    ]
)

# Shortcut functions
def info(msg: str):
    logging.info(msg)

def warning(msg: str):
    logging.warning(msg)

def error(msg: str):
    logging.error(msg)


# Example usage
if __name__ == "__main__":
    info("System started successfully.")
    warning("Low disk space detected.")
    error("Failed to connect to database.")
