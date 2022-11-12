from datetime import datetime
from datetime import date
from dateutil.parser import parse
from common.util.logging_helper import get_logger

# ---------------------------------
# Global Variable - Logger
# ---------------------------------
glogger = get_logger("api")

# ---------------------------------------------------
# Parse a string that represents date & time
# return a datetime object
# ---------------------------------------------------
def datetime_parse(dt : str) -> datetime:
    try:
        parsed_dt = parse(dt)
    except Exception as err:
        glogger.error("Failed to parse the datetime string: %s (err=%s)", dt, err)
        return None
    return parsed_dt

# ---------------------------------------------------
# Calculate age
# ---------------------------------------------------
def datetime_calc_age(dt : datetime) -> int:
    todays_date = date.today()
    age = todays_date.year - dt.year
    return age