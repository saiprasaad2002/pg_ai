import logging
from pathlib import Path
from functools import lru_cache

LOG_DIR = Path("mcp_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "pg_ai_log.log"

logging.basicConfig(
    filename=LOG_FILE, 
    format="{asctime} - {name} - {levelname} - {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    style="{"
)

@lru_cache
def get_mcp_logger():
    return logging.getLogger("mcp_logger")

