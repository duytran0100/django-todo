import logging
from typing import Optional
from logging import Logger

logger = logging.getLogger(__name__)


def get_logger(name: Optional[str] = "django") -> Logger:
    return logging.getLogger(name)
