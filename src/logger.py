import logging
import os

def setup_logger():
    """Configures the logging system for security auditing."""

    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger("MediTrust")

    # Check if the logger is already configured to avoid duplicate entries
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        # File handler (Main security log)
        file_handler = logging.FileHandler(os.path.join(log_dir, "security.log"), encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler (Optional console output)
        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(formatter)
        # logger.addHandler(stream_handler)

    return logger