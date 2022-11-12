from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from requests.utils import DEFAULT_CA_BUNDLE_PATH
from common.util import timestamp_helper
from common.util.config_wrapper import get_config_string_param, get_config_int_param
from common.util.logging_helper import get_logger as get_logger
from common.util.performance import performance_start_timer, performance_print_took_time

# -------------------------------------------------------------
# Class CosmosFactory
# -------------------------------------------------------------
class CosmosFactory():
    _instance = None


    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, keyspace_name: str = None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)


            cls._instance.glogger = get_logger("CosmosFactory")
            cls._instance.glogger.debug("Creating the instance of CosmosFactory")
            cls._instance.keyspace_name = keyspace_name
            cls._instance.session = None
            cls._instance.name = None

            # Put any initialization here.
            ssl_opts = {
                'ca_certs': DEFAULT_CA_BUNDLE_PATH,
                'ssl_version': PROTOCOL_TLSv1_2,
            }

            # -----------------------------------------------------
            # Get the configuration parameters from KV
            # -----------------------------------------------------
            try:
                if not cls._instance.keyspace_name:
                    cls._instance.keyspace_name = get_config_string_param('cosmos-keyspace')
                    cls._instance.glogger.debug("keyspace_name=%s", cls._instance.keyspace_name)

                if get_config_string_param('cosmos-certpath'):
                    ssl_opts['ca_certs'] = get_config_string_param('cosmos-certpath')
                    cls._instance.glogger.debug("ssl_opts['ca_certs']=%s", ssl_opts['ca_certs'])
            except Exception as err:
                cls._instance.glogger.error("Failed to get the conf parameters from the KV, to connect to the DB err=%s", err)
                return None

            # -----------------------------------------------------
            # Create the cosmos cluster
            # -----------------------------------------------------
            try:
                ssl_context = SSLContext(PROTOCOL_TLSv1_2)
                ssl_context.verify_mode = CERT_NONE

                auth_provider = PlainTextAuthProvider(username=get_config_string_param('cosmos-username'),
                                                      password=get_config_string_param('cosmos-password'))

                cluster = Cluster([get_config_string_param('cosmos-contact-point')],
                                  port=int(get_config_int_param('cosmos-port')),
                                  auth_provider=auth_provider, ssl_context=ssl_context, connect_timeout=600)
            except Exception as err:
                cls._instance.glogger.error("Failed to create the cosmos cluster. err=%s", err)

            # -----------------------------------------------------
            # Connect to the database
            # -----------------------------------------------------
            try:
                cls._instance.session = cluster.connect()
            except Exception as err:
                cls._instance.glogger.error("Failed to connect to the DB. err=%s", err)
                cls._instance.session = None
                cls._instance.name = None
            if not cls._instance.keyspace_name:
                cls._instance.name = "_" + timestamp_helper.get_timestamp()
                cls._instance.create_keyspace(name=cls._instance.name, strategy_type='NetworkTopologyStrategy', dc_name='datacenter',
                                     repl_factor=1)
            else:
                cls._instance.name = cls._instance.keyspace_name
                cls._instance.create_keyspace(name=cls._instance.name, strategy_type='NetworkTopologyStrategy', dc_name='datacenter',
                                     repl_factor=1)
            cls._instance.glogger.info("Connected to the COSMOS Database")

        return cls._instance

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    #@staticmethod
    #def get_instance(keyspace_name: str = None):  # Static access method.
    #    if CosmosFactory.__instance is None:
    #        CosmosFactory(keyspace_name)
    #    return CosmosFactory.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    #def __init__(self, keyspace_name : str):
    #    if CosmosFactory.__instance != None:
    #        raise Exception("This class is a singleton!")
    #        return
    #    self.glogger = get_logger("CosmosFactory")
    #    self.glogger.debug("Creating the instance of CosmosFactory")
    #    CosmosFactory.__instance = self
    #    self.keyspace_name = keyspace_name
    #    self.session = None
    #    self.name = None

    # ---------------------------------------------------------------
    # Connect to the DB - internal function
    # ---------------------------------------------------------------
    def connect_to_db(self):
        pass
        # Put any initialization here.
    #    ssl_opts = {
    #        'ca_certs': DEFAULT_CA_BUNDLE_PATH,
    #        'ssl_version': PROTOCOL_TLSv1_2,
    #    }
    #    self.session = None
    #    self.name = None

        # -----------------------------------------------------
        # Get the configuration parameters from KV
        # -----------------------------------------------------
    #    try:
    #        if not self.keyspace_name:
    #            self.keyspace_name = get_config_string_param('cosmos-keyspace')
    #            self.glogger.debug("keyspace_name=%s", self.keyspace_name)

    #        if get_config_string_param('cosmos-certpath'):
    #            ssl_opts['ca_certs'] = get_config_string_param('cosmos-certpath')
    #            self.glogger.debug("ssl_opts['ca_certs']=%s", ssl_opts['ca_certs'])
    #    except Exception as err:
    #        self.glogger.error("Failed to get the conf parameters from the KV, to connect to the DB err=%s", err)
    #        return False

        # -----------------------------------------------------
        # Create the cosmos cluster
        # -----------------------------------------------------
    #    try:
    #        ssl_context = SSLContext(PROTOCOL_TLSv1_2)
    #        ssl_context.verify_mode = CERT_NONE

    #        auth_provider = PlainTextAuthProvider(username=get_config_string_param('cosmos-username'),
    #                                              password=get_config_string_param('cosmos-password'))

    #        cluster = Cluster([get_config_string_param('cosmos-contact-point')],
    #                          port=int(get_config_int_param('cosmos-port')),
    #                          auth_provider=auth_provider, ssl_context=ssl_context, connect_timeout=600)
    #    except Exception as err:
    #        self.glogger.error("Failed to create the cosmos cluster. err=%s", err)
    #        return False

        # -----------------------------------------------------
        # Connect to the database
        # -----------------------------------------------------
    #    try:
    #        self.session = cluster.connect()
    #    except Exception as err:
    #        self.glogger.error("Failed to connect to the DB. err=%s", err)
    #        self.session = None
    #        self.name    = None
    #        return False
    #    if not self.keyspace_name:
    #        self.name = "_" + timestamp_helper.get_timestamp()
    #        self.create_keyspace(name=self.name, strategy_type='NetworkTopologyStrategy', dc_name='datacenter', repl_factor=1)
    #    else:
    #        self.name = self.keyspace_name
    #        self.create_keyspace(name=self.name, strategy_type='NetworkTopologyStrategy', dc_name='datacenter', repl_factor=1)
    #    self.glogger.info("Connected to the COSMOS Database")
    #    return True

    # ---------------------------------------------------------------
    # Get the DB session
    # ---------------------------------------------------------------
    def get_session(self):
        return self.session

    # ---------------------------------------------------------------
    # Get the Key-Space
    # ---------------------------------------------------------------
    def get_keyspace_name(self):
        return self.name

    # ---------------------------------------------------------------
    # Create the Key-Space
    # ---------------------------------------------------------------
    def create_keyspace(self, name, strategy_type, dc_name, repl_factor):
        self.glogger.debug("Creating a keyspace called: " + name)
        self.session.execute(
            'CREATE KEYSPACE IF NOT EXISTS ' + name + ' WITH replication = {\'class\': \'' + strategy_type + '\', \'' + dc_name + '\' : \'' + str(
                repl_factor) + '\' }')

    # ---------------------------------------------------------------
    # Delete the Key-Space
    # ---------------------------------------------------------------
    def delete_keyspace(self):
        self.session.execute('DROP KEYSPACE IF EXISTS ' + self.name)

# ---------------------------------------------------------------------------
# Connect to the DB
# ---------------------------------------------------------------------------
def dbwrapper_connect():
    start_time = performance_start_timer()
    cosmos = CosmosFactory.instance()
    if cosmos is None:
        return None
    cosmos.connect_to_db()
    performance_print_took_time("DB Connection", start_time)
    return cosmos

# ---------------------------------------------------------------------------
# Get DB session
# ---------------------------------------------------------------------------
def dbwrapper_get_db_session():
    cosmos = CosmosFactory.instance()
    if cosmos is None:
        return None
    return cosmos.get_session()

# ---------------------------------------------------------------------------
# Get DB keyspace name
# ---------------------------------------------------------------------------
def dbwrapper_get_db_keyspace_name():
    cosmos = CosmosFactory.instance()
    return cosmos.get_keyspace_name()
