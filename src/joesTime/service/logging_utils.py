# mypackage/logging_utils.py
import logging
import os

def setup_logging():
    log_filename = os.path.join(os.getcwd(), "joesTime_log.txt")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler for the log file
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(fh)