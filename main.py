import logging
from config.logger_setup import setup_logging

# Logging config
setup_logging()
logger = logging.getLogger(__name__)





if __name__ == "__main__":
    logger.info("Logging is set up!") #test
    