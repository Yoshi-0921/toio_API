"""Source code for the logger.

Author: Yoshinari Motokawa <yoshinari.moto@fuji.waseda.jp>
"""

from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger


def initialize_logging(name: str = __name__) -> Logger:
    """Initialize logger for logging system.

    Args:
        name (str, optional): Name of logging file.
            - Defaults to __name__.

    Returns:
        Logger: Logger to handle.
    """
    logger = getLogger(name)
    logger.propagate = False
    logger.setLevel(DEBUG)

    handler = StreamHandler()
    handler.setFormatter(
        Formatter(
            "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] \n %(message)s"
        )
    )
    handler.setLevel(DEBUG)
    logger.addHandler(handler)

    return logger
