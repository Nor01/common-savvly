import logging
import sys
import glob
from os import path
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s-%(name)s-%(funcName)s-%(lineno)d-%(levelname)s- %(message)s")
glogging_file_name = "app_log.txt"
glogging_level = "INFO"

# -----------------------------------
# The Logger global variable 
# -----------------------------------
_glogger = None

# -----------------------------------
# Get the name of the log file
# -----------------------------------
def logger_get_log_filename():
    home = str(Path.home())
    log_fname = path.join(home, glogging_file_name)
    return log_fname

# -----------------------------------------------------
# Get the list of the 'old' log files on the server
# -----------------------------------------------------
def logger_get_old_log_files():
    try:
        base_log_fname = logger_get_log_filename()
        _glogger.info("Base Log file name: %s", base_log_fname)
        files_wildcard = base_log_fname + ".20*"  # The format of the name of the old files: app_log.txt.2022-08-17
        file_list = glob.glob(files_wildcard)
        return file_list
    except Exception as err:
        _glogger.info("Exception to get the list of the old log files")
        return None

# -----------------------------------
# Log to Console
# -----------------------------------
def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

# -----------------------------------
# Log to File
# -----------------------------------
def _get_file_handler(logger_name):
    log_fname = logger_get_log_filename()
    file_handler = TimedRotatingFileHandler(log_fname, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler

# -----------------------------------
# Get the logger object
# -----------------------------------
def get_logger(logger_name=""):
    global _glogger
    if not _glogger:
        logger = logging.getLogger(logger_name)
        logger.setLevel(glogging_level)  # better to have too much log than not enough
        logger.addHandler(_get_console_handler())
        logger.addHandler(_get_file_handler(logger_name))
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        _glogger = logger
        logger.debug("Logger Started for %s", logger_name)
    return _glogger
