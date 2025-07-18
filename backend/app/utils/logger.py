"""
AutoShield Logging Utility
Centralized logging configuration and utilities
"""

import logging
import sys
from typing import Optional
from app.core.config import get_settings

settings = get_settings()

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

# Create formatter
formatter = logging.Formatter(LOG_FORMAT)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

def setup_logging():
    """
    Setup application-wide logging configuration
    """
    # Configure root logger
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[console_handler]
    )
    
    # Set uvicorn logger level
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(LOG_LEVEL)
    
    # Set sqlalchemy logger level (reduce verbosity)
    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(logging.WARNING)
    
    # Set web3 logger level (reduce verbosity)
    web3_logger = logging.getLogger("web3")
    web3_logger.setLevel(logging.WARNING)

# Setup logging on import
setup_logging()
