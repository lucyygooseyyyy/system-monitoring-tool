import json
import logging
import os
from config import LOG_DIR, LOG_FILE

os.makedirs(LOG_DIR, exist_ok = True)

logging.basicConfig(
    filename = LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_stats(stats:dict) -> None:
    """Save system stats to the log file."""
    logging.info(json.dumps(stats))

def log_alert(message: str) -> None:
    """Save alert messages to the log file."""
    logging.warning(message)
