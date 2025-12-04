import logging
import sys
from datetime import datetime

def setup_logging():
    """Configure logging."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()