import os
import logging
import logging.handlers as handler

import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, 'init_water_app/.env'))
environ.Env.read_env()

# TODO
# LOG_NAME = env("LOG_NAME")
# LOG_FILE_LOCATION = str(BASE_DIR) + env("LOG_FILE_LOCATION")
# LOG_FORMAT = env("LOG_FORMAT")
# LOG_LEVEL = env("LOG_LEVEL")

LOG_NAME = "iwater_log"
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_FILE_LOCATION = str(BASE_DIR) + "/iwater/log_files/iwater.log"

LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logger = logging.getLogger(LOG_NAME)
try:
    # Setup the logger
    log_handler = handler.RotatingFileHandler(LOG_FILE_LOCATION, maxBytes=10*1024*1024, backupCount=20)
    formatter = logging.Formatter(LOG_FORMAT)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)

    # Set logging level
    level = logging.getLevelName(LOG_LEVEL)
    if level:
        logger.setLevel(level)
    else:
        logger.setLevel(logging.DEBUG)

except (IOError, ValueError) as err:
    # If logging error happened, system logic needs to pass in order to avoid system crash
    # Therefore, system will not log anything
    # TODO: Think about how system can handle logging error
    # print(err)
    # logger.exception(err)
    pass
