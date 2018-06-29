import logging
import os
import multiprocessing

def initializeLog():
    
    logger = logging.getLogger('queue_log')
    logger.setLevel(logging.DEBUG)
    logFormat = "%(asctime)s | %(levelname)s | %(message)s"
    datetimefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(logFormat, datetimefmt)
    #set up file logging
    '''
    logFile = "\Users\Ed\Documents\PythonWork\logging\event.log"
    fh = logging.FileHandler(logFile)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    '''
    #set up terminal logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)