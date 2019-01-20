import errno
import logging  #@UnusedImport # @ImportRedefinition
import logging.handlers
import os
from inspect import currentframe

__all__ = ['mylog', 'get_linenumber']
global mylog


#from logging import *
logging._levelToName = {
    logging.CRITICAL: 'CRITC',
    logging.ERROR:    'ERROR',
    logging.WARNING:  'WARN',
    logging.INFO:     'INFO',
    logging.DEBUG:    'DEBUG',
    logging.NOTSET:   'NOTSET',
}
format_hdlr = "%(asctime)s %(levelname)4s:%(lineno)4s - %(module)22s %(funcName)15s() %(message)s  "
#format_hdlr = "%(levelname)5s %(lineno)4s - %(module)22s %(funcName)15s() %(message)s  %(threadName)s "

try:
    os.mkdir('log')
except OSError as e:
    if e.errno != errno.EEXIST:
        print ("creating directory 'log'  OSError %s" % e)


try:
    os.remove(os.path.join("log", "db2.log"))
except:
    pass

try:
    os.remove(os.path.join("log", "db2.log.1"))
except:
    pass


try:
    os.remove(os.path.join("log", "db2.log.2"))
except:
    pass

try:
    os.remove(os.path.join("log", "db2.log.3"))
except:
    pass

try:
    os.remove("traces.log")
except:
    pass

hdlr = logging.handlers.RotatingFileHandler(os.path.join("log", "db2.log"), maxBytes=20000000, backupCount=3)
hdlr.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(format_hdlr)
ch.setFormatter(formatter)
hdlr.setFormatter(formatter)

mylog     = logging.getLogger(__name__)
mylog.addHandler(ch)
mylog.addHandler(hdlr)
mylog.setLevel(logging.INFO)

mylog.info("loggers initialized")

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno