# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, Formatter, DEBUG


def initialize_logging(name):
    logger = getLogger(name)
    logger.propagate = False
    logger.setLevel(DEBUG)

    handler = StreamHandler()
    handler.setFormatter(Formatter('[%(levelname)s] [%(asctime)s] [%(filename)s] \n %(message)s'))
    handler.setLevel(DEBUG)
    logger.addHandler(handler)

    return logger
