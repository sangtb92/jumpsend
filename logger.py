import logging
from config import BaseConfig
from datetime import datetime


class Logger():
    def __init__(self):
        logs_file = BaseConfig.LOGGING_DIR + str(datetime.now().date()) + ".logs"
        logging.basicConfig(format='%(levelname)s : %(message)s', filename=logs_file, level=logging.DEBUG)

    def write_log(self, level, message):
        log_time = str(datetime.now())
        msg = log_time + " : " + message
        if level.upper() == "DEBUG":
            logging.debug(msg)
        elif level.upper() == "INFO":
            logging.info(msg)
        elif level.upper() == "WARNING":
            logging.warning(msg)
