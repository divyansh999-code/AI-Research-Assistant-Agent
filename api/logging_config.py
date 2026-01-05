import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_requests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("API")

def log_request(endpoint: str, api_key_info: dict, query: str = None):
    """Log API requests"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "user": api_key_info.get("name", "Unknown"),
        "usage": f"{api_key_info.get('usage', 0)}/{api_key_info.get('limit', 0)}",
        "query": query[:100] if query else None  # Truncate long queries
    }
    logger.info(json.dumps(log_data))
