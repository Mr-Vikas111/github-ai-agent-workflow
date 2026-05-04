"""Logging configuration."""

import logging


def configure_logging() -> None:
    """Configure a simple structured logging format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
