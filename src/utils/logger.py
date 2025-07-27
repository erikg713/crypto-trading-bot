import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# Optional: colorized logs in console
try:
    from colorlog import ColoredFormatter
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False


def get_logger(name: str = "app", level: int = logging.DEBUG) -> logging.Logger:
    """
    Returns a logger instance with console and file handlers configured.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        return logger  # Avoid adding multiple handlers

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir / f"{name}.log"

    # File handler with rotation
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8"
    )
    file_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if COLORLOG_AVAILABLE:
        console_format = ColoredFormatter(
            fmt='%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
    else:
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
    console_handler.setFormatter(console_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

