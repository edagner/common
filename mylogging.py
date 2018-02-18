import logging
import os

def initializeLog(datestring):
    logFile = "\Users\Ed\Documents\PythonWork\{}event.log".format(datestring)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logFormat = "%(asctime)s | %(levelname)s | %(message)s"
    datetimefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(logFormat, datetimefmt)
    #set up file logging
    fh = logging.FileHandler(logFile)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    #set up terminal logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)