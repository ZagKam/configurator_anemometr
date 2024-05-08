from logging import Logger
import logging


logger = Logger("__main__")
stream_handler = logging.StreamHandler()
fileHandler = logging.FileHandler("program.log")

formatter = logging.Formatter(fmt=' %(name)s :: %(funcName)s :: %(levelname)-8s :: %(message)s')

stream_handler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
