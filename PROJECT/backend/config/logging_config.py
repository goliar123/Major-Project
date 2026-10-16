"""
Logging configuration for Failure Attribution system.
"""
import logging
import sys
from rich.logging import RichHandler

def setup_logger(name: str = "attribution") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        console_handler = RichHandler(rich_tracebacks=True, show_time=True, show_path=False)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

logger = setup_logger()
