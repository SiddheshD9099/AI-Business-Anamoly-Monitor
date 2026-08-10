import logging
from pathlib import Path


# ======================================================
# PROJECT PATH
# ======================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# ======================================================
# LOG DIRECTORY
# ======================================================

LOG_DIR = (
    BASE_DIR / "logs"
)

LOG_DIR.mkdir(
    exist_ok=True
)


# ======================================================
# LOG FILE
# ======================================================

LOG_FILE = (
    LOG_DIR
    / "application.log"
)


# ======================================================
# LOGGER
# ======================================================

logger = logging.getLogger(
    "business_anomaly_monitor"
)

logger.setLevel(
    logging.INFO
)


# Prevent duplicate handlers if Streamlit
# reloads the application.

if not logger.handlers:

    formatter = logging.Formatter(
        "[%(asctime)s] "
        "%(levelname)s "
        "%(name)s: "
        "%(message)s"
    )

    file_handler = (
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

