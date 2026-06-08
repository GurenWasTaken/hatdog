import logging
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "fb_tool.log")


def get_logger(enabled=True):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logger = logging.getLogger("fb_tool")
    logger.setLevel(logging.DEBUG if enabled else logging.CRITICAL)

    if not logger.handlers:
        fh = logging.FileHandler(LOG_PATH)
        fh.setLevel(logging.DEBUG)
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
