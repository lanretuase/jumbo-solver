"""Structured logging configuration."""

import logging
import sys

from app.config import get_settings


def setup_logging() -> None:
    """Configure structured logging for the application.

    Uses a JSON-like format with timestamp, level, logger name, and message.
    The log level is read from application settings.
    """
    settings = get_settings()

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s"
    )
    date_format = "%Y-%m-%dT%H:%M:%S%z"

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    # Quieten noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
