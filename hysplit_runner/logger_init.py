import sys
import logging
import os

LOG_MODE = 'DEBUG'
LOGFILE = 'log'
PROJECTDIR = os.path.dirname(os.path.realpath(__file__))


def logger_def():
    """
    initialize the logger
    """

    logFile = os.path.join(PROJECTDIR, LOGFILE)
    logModeDict = {
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR
        }
    logger = logging.getLogger(__name__)
    logger.setLevel(logModeDict[LOG_MODE])

    fh = logging.FileHandler(logFile)
    fh.setLevel(logModeDict[LOG_MODE])
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logModeDict[LOG_MODE])

    formatterFh = logging.Formatter('%(asctime)s - %(name)s - ' +
                                    '%(funcName)s - %(lineno)d - %(message)s')
    formatterCh = logging.Formatter('%(message)s')
    fh.setFormatter(formatterFh)
    ch.setFormatter(formatterCh)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger
