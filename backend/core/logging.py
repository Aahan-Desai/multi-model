import logging
from typing import Optional

from backend.core.config import settings


_LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """
    Configure the application's root logger.

    This function is idempotent and safe to call multiple times.
    """

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format=_LOG_FORMAT,
        datefmt=_DATE_FORMAT,
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Usually __name__ from the calling module.

    Returns:
        A logger instance.
    """

    return logging.getLogger(name)