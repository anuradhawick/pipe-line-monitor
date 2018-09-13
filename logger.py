import logging
import sys
import os
from os import path

log_file_name = "my_actions_log.log"

def log(message, level):

    # Initialize logger file
    if not path.exists(log_file_name):
        open(log_file_name, 'a')

    rootLogger = logging.getLogger("my_logger")

    if not rootLogger.handlers:

        # Logger configurations
        logFormatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s")
        rootLogger.setLevel(logging.INFO)

        # Set file handler
        fileHandler = logging.FileHandler(log_file_name)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        # Set console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

   # Separate messages from log level
    if level == 'DEBUG':
        rootLogger.debug(message)
    elif level == 'INFO':
        rootLogger.info(message)
    elif level == 'WARNING':
        rootLogger.warning(message)
