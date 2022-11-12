import os
import os.path
from common.util.json_builder import JsonBuilder
from common.util.logging_helper import get_logger
#from common.util.utility_functions import find_file_path, utils_is_dev_env
from common.util.utility_functions import utils_is_dev_env

# -------------------------------------------------------------------------------------
#  This is a singleton object.  We do not need more than one instance of this class.
# -------------------------------------------------------------------------------------
class ReadConfig:
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance(config_path : str = None):  # Static access method.
        if ReadConfig.__instance is None:
            ReadConfig(config_path)
        return ReadConfig.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, config_path : str):
        if ReadConfig.__instance != None:
            raise Exception("This class is a singleton!")
            return
        ReadConfig.__instance = self
        if config_path is None:
            raise Exception("The configuration path must be valid. It cannot be None")
        self.glogger = get_logger("config")
        self.cred = None
        builder = JsonBuilder()
        if utils_is_dev_env():
            filepath = config_path + "configuration-dev.json"
            #filepath = self._find_config_file("configuration-dev.json")
            #self.glogger.info("DEV configuration file is being used: %s", filepath)
        else:
            filepath = config_path + "configuration.json"
            #filepath = self._find_config_file("configuration.json")
            #self.glogger.info("PROD configuration file is being used: %s", filepath)
        if self._config_file_exists(filepath):
            self.glogger.info("The following configuration file is being used: %s", filepath)
        else:
            raise Exception("Configuration file not found!: " + filepath)  # We are not supposed to get here.
       #if not filepath:
       #     self.glogger.error("Config File not found: %s", filepath)
       #     raise Exception("Configuration file not found!") # We are not supposed to get here.
       #else:
       #     self.glogger.info("PROD configuration file is being used: %s", filepath)
        builder = builder.load_json(filepath)
        self.cred = builder.raw()

    # -----------------------------------------------------------------
    # Check if the configuration file exits
    # -----------------------------------------------------------------
    def _config_file_exists(self, filename: str):
        if os.path.isfile(filename):
            return True
        self.glogger.info("The configuration file does not exist: %s", filename)
        return False

    # -----------------------------------------------------------------
    # Find the configuration file
    # -----------------------------------------------------------------
    #def _find_config_file(self, filename: str = "configuration-dev.json"):
    #    # filename = 'configuration.json'
    #    filepath = os.getcwd() + "/" + filename
    #    if not os.path.isfile(filepath):
    #        filepath = os.path.dirname(__file__) + "/" + filename
    #        if not os.path.isfile(filepath):
    #            filepath = find_file_path(filename, os.path.dirname(__file__) + "/../../")
    #            if not filepath:
    #                self.glogger.error("I was not able to find the config file (%s)... exiting....", filename)
    #                exit(-1)
    #    self.glogger.info("Found config file: %s", filepath)
    #    return filepath

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
            self.glogger.debug("The parameter %s not found in the config parameters. Look in the KV", name)
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
        conf.glogger.debug("The parameter %s not found in the config parameters. Looking in the KV", name)
        #return default
        return AzureKeyVaultWrapper.get_instance().get_string_param(name, default)

# ------------------------------------------------------
# Init Configuration
# ------------------------------------------------------
def config_wrapper_init(config_path : str):
    ReadConfig.get_instance(config_path)

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
# Set/Get if we are logging the CQL Query Results
# ---------------------------------------------------------------------------
def config_log_cql_results():           return True if get_config_string_param("log_cql_results") == 'True' else False

def config_set_log_cql_results(log_cql_res):
    if log_cql_res:
        set_config_string_param("log_cql_results", 'True')
    else:
        set_config_string_param("log_cql_results", 'False')

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

# ---------------------------------------------------------------------------
# Set/Get if we are logging the session
# ---------------------------------------------------------------------------
def config_log_session():           return True if get_config_string_param("log_session") == 'True' else False
def config_set_log_session(log_sess):
    if log_sess:
        set_config_string_param("log_session", 'True')
    else:
        set_config_string_param("log_session", 'False')

# ---------------------------------------------------------------------------
# Set/Get if we are logging the session
# ---------------------------------------------------------------------------
def config_log_request():           return True if get_config_string_param("log_requset") == 'True' else False
def config_set_log_request(log_req):
    if log_req:
        set_config_string_param("log_requset", 'True')
    else:
        set_config_string_param("log_requset", 'False')

# ---------------------------------------------------------------------------
# Get the B2C Domain name
# ---------------------------------------------------------------------------
def config_get_b2c_domain_name():
    tenant = get_config_string_param("b2c_tenantName")
    domain_template = get_config_string_param("b2c_domainName_template")
    return domain_template.format(tenant=tenant)

# ---------------------------------------------------------------------------
#Get the default password fro a new created user
# ---------------------------------------------------------------------------
def config_get_b2c_new_user_default_password():
    return get_config_string_param("b2c_new_user_password")
