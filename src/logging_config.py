"""Central logging configuration with file rotation.

Creates a rotating file log and keeps at least 3 old rotated log files.
"""

from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)


def _configure_logging() -> None:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel("DEBUG")
    file_handler.setFormatter(formatter)

    root_logger.setLevel("DEBUG")
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


_configure_logging()
