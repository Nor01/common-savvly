from common.util.logging_helper import get_logger
from auth.absauth import *
from auth.oauth import *
from auth.activedir import *
from auth.flasklogin import *

# -------------------------------------------------------------------------------------------------
# Class Auth
# -------------------------------------------------------------------------------------------------
class Auth():
    auth_method_oauth      = 1   # We are using the OAUTH2 method for authentication
    auth_method_activedir  = 2   # We are using the ACTIVEDIR method for authentication
    auth_method_flasklogin = 3   # We are using the FLASKLOGIN method for authentication
    __instance = None

    ## ---------------------------------------------
    ## Return the singletone object
    ## ---------------------------------------------
    @staticmethod
    def get_instance(auth_method = None, app = None):  # Static access method.
        if Auth.__instance is None:
            Auth(auth_method, app)
            Auth.__instance.glogger.debug("First time creation of Auth. method=%d", auth_method)
        return Auth.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, auth_method, app):
        if Auth.__instance != None:
            raise Exception("This class is a singleton!")
            return
        Auth.__instance = self
        self.auth_method  = auth_method
        self.glogger = get_logger()
        self.glogger.debug("Creating the instance of Auth of type %d", auth_method)

        if  self.auth_method  == Auth.auth_method_oauth:
            self.authobj = Oauth.get_instance(app)
        elif self.auth_method  == Auth.auth_method_activedir:
            self.authobj = ActiveDir.get_instance(app)
        elif self.auth_method  == Auth.auth_method_flasklogin:
            self.authobj = FlaskLogin.get_instance(app)
        else:
            self.authobj = FlaskLogin.get_instance(app) # Create this type by default
            self.glogger.error("Invalid authentication method: %s", str(auth_method))
            #raise Exception("Invalid Authentication Method. It must be configured before creating the Auth object")

## -----------------------------------------------------------------------------
## The public functions that must be implemented by the authentication object
## -----------------------------------------------------------------------------
def auth_init(auth_method, app):        Auth.get_instance(auth_method, app)
#def auth_start_login():                  return Auth.get_instance().authobj.start_login_process()
#def auth_start_register_user():          return Auth.get_instance().authobj.start_register_user_process()
#def auth_start_register_ria():           return Auth.get_instance().authobj.start_register_ria_process()
#def get_user_flow_url(flow=None):        return Auth.get_instance().authobj.get_user_flow_url(flow)
def auth_check_result():                 return Auth.get_instance().authobj.check_result()
def auth_post_logout():                  return Auth.get_instance().authobj.post_logout()
def auth_get_current_userid():           return Auth.get_instance().authobj.get_current_userid()
def auth_parse_access_token():           return Auth.get_instance().authobj.parse_access_token()
def auth_get_login_url():                return Auth.get_instance().authobj.get_login_url()
def auth_get_register_user_url():        return Auth.get_instance().authobj.get_register_user_url()
def auth_get_register_advisor_url():     return Auth.get_instance().authobj.get_register_advisor_url()