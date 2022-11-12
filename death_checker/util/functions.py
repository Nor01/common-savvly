import os
from pathlib import Path


from death_checker.util.check_log import get_logger

# ---------------------------------
# Global Variable - Logger
# ---------------------------------
glogger = get_logger("api")

# ---------------------------------------------------
# Are we in PROD environment or Dev environment
# ---------------------------------------------------
def utils_is_dev_env():
    runenv = "dev"
    try:
        runenv = os.environ['API_ENVIRONMENT']
    except KeyError:
        glogger.error("Environment variable (API_ENVIRONMENT) required - assuming it is dev otherwise")
        os.environ['API_ENVIRONMENT'] = runenv
        return True
    if runenv == "dev":
        return True  # Dev Environment
    return False  # Product Environment


