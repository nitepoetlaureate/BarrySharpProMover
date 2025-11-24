#!/usr/bin/env python3
"""
Centralized Logging Configuration
Provides consistent logging setup for all BarrySharpProMover scripts.

Usage:
    from scripts.logging_config import setup_logging
    logger = setup_logging(__name__)
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


def setup_logging(
    name: str,
    log_level: Optional[str] = None,
    log_to_file: bool = True,
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Configure logging for BarrySharpProMover scripts.

    Args:
        name: Logger name (typically __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                  If None, reads from LOG_LEVEL environment variable or defaults to INFO
        log_to_file: Whether to log to file in addition to console
        log_dir: Directory for log files. If None, uses project_root/logs

    Returns:
        Configured logger instance
    """
    # Determine log level
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatters
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (with rotation)
    if log_to_file:
        # Determine log directory
        if log_dir is None:
            project_root = Path.cwd()
            log_dir = project_root / 'logs'

        # Create log directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create rotating file handler
        log_file = log_dir / f"{name.replace('.', '_')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def set_verbose(logger: logging.Logger, verbose: bool = True):
    """
    Enable verbose/debug logging.

    Args:
        logger: Logger instance to modify
        verbose: If True, set to DEBUG level
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)


# Example usage
if __name__ == "__main__":
    # Demo logging
    logger = setup_logging(__name__)

    logger.debug("This is a debug message (won't show by default)")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    print("\n--- Verbose mode ---")
    set_verbose(logger, True)
    logger.debug("Now debug messages will show")
