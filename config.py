import logging

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s - %(filename)s'
LOG_LEVEL = logging.INFO  # Can be changed to INFO, WARNING, ERROR, or CRITICAL

def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler('application.log'),
            logging.StreamHandler()  # Optional, to print to console as well
        ]
    )
