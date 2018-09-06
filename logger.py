import logging
import sys

def log(message, level):

    # Logger file
    open('my_actions_log.log', 'a')

    # Logger configurations
    logging.basicConfig(
        # stream=sys.stdout,
        filename='my_actions_log.log',
        format='%(asctime)s %(levelname)s %(message)s',
        level=logging.INFO
    )

    # TODO add both logging to file and console

    # Separate messages from log level
    if level == 'DEBUG':
        logging.debug(message)
    elif level == 'INFO':
        logging.info(message)
    elif level == 'WARNING':
        logging.warning(message)