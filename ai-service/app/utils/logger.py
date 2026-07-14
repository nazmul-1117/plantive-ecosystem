import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs folder if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "ai_service.log")

# Configure logging
logger = logging.getLogger("ai_service")
logger.setLevel(logging.INFO)  # INFO for normal logs, DEBUG for detailed logs

# Rotating file handler (10MB per file, keep 5 backups)
handler = RotatingFileHandler(LOG_FILE, maxBytes=10_000_000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Optional: also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)