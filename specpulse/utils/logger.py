"""
SpecPulse Logging Infrastructure
File-based logging with rotation for production use
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os


def setup_logger(project_path: Path, verbose: bool = False) -> logging.Logger:
    """
    Setup file and console logging for SpecPulse

    Args:
        project_path: Path to project root
        verbose: Enable DEBUG level logging

    Returns:
        Configured logger instance
    """
    # Create logs directory
    log_dir = project_path / '.specpulse' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'specpulse.log'

    # Determine log level
    level = logging.DEBUG if verbose else logging.INFO

    # Override with environment variable if set
    env_level = os.environ.get('SPECPULSE_LOG_LEVEL', '').upper()
    if env_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        level = getattr(logging, env_level)

    # File handler with rotation (10MB max, 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler (errors only unless verbose)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR if not verbose else logging.DEBUG)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # Get or create logger
    logger = logging.getLogger('specpulse')
    logger.setLevel(level)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log initialization
    logger.info(f"SpecPulse logger initialized (level={logging.getLevelName(level)})")
    logger.debug(f"Log file: {log_file}")

    return logger


def get_logger() -> logging.Logger:
    """Get the SpecPulse logger instance"""
    return logging.getLogger('specpulse')
