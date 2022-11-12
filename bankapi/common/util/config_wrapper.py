import os

from common.util.json_builder import JsonBuilder
from common.util.logging_helper import get_logger
from common.util.utility_functions import find_file_path, utils_is_dev_env


# -------------------------------------------------------------------------------------
#  This is a singleton object.  We do not need more than one instance of this class.
# -------------------------------------------------------------------------------------
class ReadConfig:
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if ReadConfig.__instance is None:
            ReadConfig()
        return ReadConfig.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
        if ReadConfig.__instance != None:
            raise Exception("This class is a singleton!")
            return
        ReadConfig.__instance = self
        self.glogger = get_logger("config")
        self.cred = None
        builder = JsonBuilder()
        if utils_is_dev_env():
            filepath = self._find_config_file("configuration-dev.json")
            self.glogger.info("DEV configuration file is being used: %s", filepath)
        else:
            filepath = self._find_config_file("configuration.json")
            self.glogger.info("PROD configuration file is being used: %s", filepath)
        if not filepath:
            self.glogger.error("Config File not found: %s", filepath)
            raise Exception("Configuration file not found!") # We are not supposed to get here.
        builder = builder.load_json(filepath)
        self.cred = builder.raw()

    # -----------------------------------------------------------------
    # Find the configuration file
    # -----------------------------------------------------------------
    def _find_config_file(self, filename: str = "configuration-dev.json"):
        # filename = 'configuration.json'
        filepath = os.getcwd() + "/" + filename
        if not os.path.isfile(filepath):
            filepath = os.path.dirname(__file__) + "/" + filename
            if not os.path.isfile(filepath):
                filepath = find_file_path(filename, os.path.dirname(__file__) + "/../../")
                if not filepath:
                    self.glogger.error("I was not able to find the config file (%s)... exiting....", filename)
                    exit(-1)
        self.glogger.info("Found config file: %s", filepath)
        return filepath

    # -----------------------------------------------------------------
    # Read a  paramter of string type from the configuration
    # -----------------------------------------------------------------
    def get_string_value(self, name: str, default: str = "") -> str:
        if name in self.cred.keys():
            return self.cred[name]
        else:
            return default

    # -----------------------------------------------------------------
    # Read a  paramter of INT type from the configuration
    # -----------------------------------------------------------------
    def get_int_value(self, name: str, default: int = "") -> int:
        v = self.get_string_value(name, str(default))
        try:
            return int(v)
        except:
            get_logger("config").error("Returned value for {} is not an int".format(name))
            return int(default)

    # -----------------------------------------------------------------
    # Write a  paramter of string type to the configuration
    # -----------------------------------------------------------------
    def set_string_value(self, name: str, value: str):
        self.cred[name] = value

    def _get_config(self):
        return self.cred

    def is_param_local(self, name: str):
        if name in self.cred.keys():
            return True
        else:
            return False

# ------------------------------------------------------
# Get a string parameter from the configuration
# ------------------------------------------------------
def get_config_string_param(name: str, default: str = "") -> str:
    from common.kv.kv_wrapper import AzureKeyVaultWrapper
    conf = ReadConfig.get_instance()
    if conf.is_param_local(name):
        return conf.get_string_value(name, default)
    else:
        #return default
        return AzureKeyVaultWrapper.get_instance().get_string_param(name, default)

# ------------------------------------------------------
# Get a int parameter from the configuration
# ------------------------------------------------------
def get_config_int_param(name: str, default: int = 0) -> int:
    from common.kv.kv_wrapper import AzureKeyVaultWrapper
    conf = ReadConfig.get_instance()
    if conf.is_param_local(name):
        return conf.get_int_value(name, default)
    else:
        #return default
        return AzureKeyVaultWrapper.get_instance().get_int_param(name, default)

# ------------------------------------------------------
# Set a string parameter to the configuration
# ------------------------------------------------------
def set_config_string_param(name: str, value: str):
    return ReadConfig.get_instance().set_string_value(name, value)

# ---------------------------------------------------------------------------
# Set/Get if we are in DEV environment
# ---------------------------------------------------------------------------
def config_is_dev_mode():             return True if get_config_string_param("is_dev_mode") == 'True' else False

def config_set_dev_mode(is_dev_env):
    if is_dev_env:
        set_config_string_param("is_dev_mode", 'True')
    else:
        set_config_string_param("is_dev_mode", 'False')

# ---------------------------------------------------------------------------
# Set/Get if we are in DEBUG Mode
# ---------------------------------------------------------------------------
def config_is_debug_mode():              return True if get_config_string_param("is_debug_mode") == 'True' else False

def config_set_debug_mode(is_debug):
    if is_debug:
        set_config_string_param("is_debug_mode", 'True')
    else:
        set_config_string_param("is_debug_mode", 'False')

# ---------------------------------------------------------------------------
# Set/Get if we are logging the CQL Query commands
# ---------------------------------------------------------------------------
def config_log_cql_commands():           return True if get_config_string_param("log_cql_commands") == 'True' else False

def config_set_log_cql_commands(log_cql_cmd):
    if log_cql_cmd:
        set_config_string_param("log_cql_commands", 'True')
    else:
        set_config_string_param("log_cql_commands", 'False')

# ---------------------------------------------------------------------------
# Set/Get if we are logging the CQL Query commands
# ---------------------------------------------------------------------------
def config_is_admin_mode():           return True if get_config_string_param("admin_mode") == 'True' else False

def config_set_admin_mode(isadmin):
    if isadmin:
        set_config_string_param("admin_mode", 'True')
    else:
        set_config_string_param("admin_mode", 'False')

# ---------------------------------------------------------------------------
# Set/Get if we are logging the 'Took-Time'
# ---------------------------------------------------------------------------
def config_log_took_time():           return True if get_config_string_param("log_took_time") == 'True' else False

def config_set_log_took_time(log_took_time):
    if log_took_time:
        set_config_string_param("log_took_time", 'True')
    else:
        set_config_string_param("log_took_time", 'False')
