import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(logs_dir / "app.log", mode='a')
    ]
)

# Create logger for this module
logger = logging.getLogger(__name__)

# Create specific loggers for different parts of the application
api_logger = logging.getLogger("api")
crud_logger = logging.getLogger("crud")
db_logger = logging.getLogger("database")
schema_logger = logging.getLogger("schemas")