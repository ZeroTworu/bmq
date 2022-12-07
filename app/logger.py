import logging
import re
from os import getenv


def get_logger(name: str):
    level: str = getenv('BMQ_LOG_LEVEL', 'INFO').upper()
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter(fmt='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(level))
    logger.addHandler(handler)
    return logger


def censor_amqp(dsn: str) -> str:
    return re.sub(':[A-z0-9]+@', '@***:', dsn)
