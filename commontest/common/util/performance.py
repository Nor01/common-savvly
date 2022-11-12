import datetime
from common.util.config_wrapper import *

# ---------------------------------------------------------------------
# Create an instrance of the logger (This must be before our imports )
# ----------------------------------------------------------------------
from common.util.logging_helper import get_logger
glogger = get_logger("perf")

# ------------------------------------------------------
# Start a timer to measure a set of operations
# ------------------------------------------------------
def performance_start_timer():
    return datetime.datetime.now()

# ------------------------------------------------------
# Start a timer to measure a set of operations
# ------------------------------------------------------
def performance_print_took_time(label, start_time) -> str:
    end_time = datetime.datetime.now()
    tooktime = end_time - start_time
    duration = str(tooktime.seconds) + "." + str(int(tooktime.microseconds / 1000))
    if config_log_took_time():
        glogger.info("%s: Took %s seconds", label, duration)
    return duration
