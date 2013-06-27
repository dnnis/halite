""" Aiding package of Utility Helper Objects """
import os
from os import path
import datetime
import logging

""" Logging aids
    usage:
    import aiding
    logger = aiding.getLogger(name="Demo",level=aiding.LOGGING_LEVELS['debug'])
"""
LOGGING_LEVELS = dict(debug=logging.DEBUG, info=logging.INFO, warning=logging.WARNING,
                  error=logging.ERROR, critical=logging.CRITICAL)    

LOGGER_NAME = "Halide" # default logger name
LOGGER_LEVEL = logging.INFO # default logger level
LOGGER_FORMAT = '%(asctime)s %(name)s: %(message)s'
LOGGER_DATE_FORMAT ='%Y%m%d_%H%M%S.%f'

class SpecialFormatter(logging.Formatter):
    """ Special formatter to allow using microseconds in log format.
        Uses datetime object instead of ctime struct so %f works in strftime
    """
    converter= datetime.datetime.fromtimestamp
    
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s


LOGGER_FORMATTER = SpecialFormatter(LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT) 
LOGGER_HANDLER = logging.StreamHandler()
LOGGER_HANDLER.setFormatter(LOGGER_FORMATTER)

def getLogger(name=LOGGER_NAME, level=LOGGER_LEVEL):
    """ Utility fuction for creating logger with predefined configuration
        Call getLogger() with the same name to get the same logger object
    
    """
    logger = logging.getLogger(name)
    logger.addHandler(LOGGER_HANDLER)
    logger.propagate = False 
    logger.setLevel(level)
    return logger


""" File aids

"""

def getFiles(top, prefix):
    """ Returns tuple of scripts and styles lists generated by
        walking down directory tree starting at top  and appending
        all filenames with extension .js to scripts and
        all filenames with extension .css to styles
        the filenames returned are the relative paths to top with prefix prefixed
        This allows remapping file names to a different tree
    """
    scripts = []
    styles = []
    for dirpath, dirnames, filenames in os.walk(path.abspath(top)):
        for  fname in filenames:
            root, ext = path.splitext(fname)
            if ext == '.js':
                scripts.append(dict(name=path.join(prefix,
                            path.relpath(path.join(dirpath, fname), top))))
            elif ext == '.css':
                styles.append(dict(name=path.join(prefix,
                            path.relpath(path.join(dirpath, fname), top))))
    return (scripts, styles)