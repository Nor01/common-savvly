import flask_login
from flask import session
from flask import Flask, request, redirect
from common.util.logging_helper import get_logger
from auth.absauth import *


# ---------------------------------------------
# A class represinting the Flask-login session
# ----------------------------------------------
class UserSession(flask_login.UserMixin):
    pass

# -------------------------------------------------------------------------------------------------
# Class FlaskLogin
# -------------------------------------------------------------------------------------------------
class FlaskLogin(AbsAuth):
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance(app):  # Static access method.
        if FlaskLogin.__instance is None:
            FlaskLogin(app)
        return FlaskLogin.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, app):
        if FlaskLogin.__instance != None:
            raise Exception("This class is a singleton!")
            return
        super().__init__(app)
        FlaskLogin.__instance = self
        self.glogger = get_logger()
        self.glogger.info("Creating the instance of FlaskLogin")

        # -----------------------------------------------------------------------------------
        # Setup up a Flask instance and support server-side sessions using Flask-Session
        # -----------------------------------------------------------------------------------
        self._login_manager = flask_login.LoginManager()
        self._login_manager.init_app(self.app)

        # ----------------------------------------------------------------------
        #Register our function to Flask-Login
        # ----------------------------------------------------------------------
        self._login_manager.user_loader(self._load_user)
        self._login_manager.request_loader(self._request_loader)

    # -------------------------------------------------------
    # Must be implemented by the child
    # Returns:
    #  redirect_url : URL to forward to do the authentication
    # -------------------------------------------------------
    def _get_user_flow_url(self, flow=None):
        user_session = self._load_from_request(request)
        if user_session:
            self.glogger.info("The user created. Lets redirect to authenticate")
            flask_login.login_user(user_session)
            redirect_url = self.get_authorized_uri()
            return redirect_url
        self.glogger.error("Failed to create user. We are not going to redirect")
        return None

    # -------------------------------------------------------
    # Must be implemented by the child
    # -------------------------------------------------------
    def check_result(self, flow=None):
        if self.get_current_userid():
            self.glogger.error("The user already exists in the session. Authenticated")
            return True   # The user is logged in
        self.glogger.error("Not Authenticated")
        return False      # Authentication failed

    # -------------------------------------------------------
    # Must be implemented by the child
    # -------------------------------------------------------
    def post_logout(self):
        flask_login.logout_user()
        self._clear_userid_object()

    # -----------------------------------
    # Get the current logged-in user
    # -----------------------------------
    def get_current_userid(self):
        if flask_login.current_user:
            return flask_login.current_user.get_id()
        return None

    # ---------------------------------------------
    # Extenal functions - To BE MOVED to other modules
    # ----------------------------------------------
    def _user_exists(self, user_id):
        self.glogger.error("This function is not implemented yet. user_id=%s", user_id)
        return True

    # ---------------------------------------------
    # Extenal functions - To BE MOVED to other modules
    # ----------------------------------------------
    def _authenticate(self, user_id, password):
        self.glogger.error("This function is not implemented yet. user_id=%s password=%s", user_id, password)
        return True

    # ---------------------------------------------
    # Get user-session from the memory
    # ----------------------------------------------
    def _get_user_from_memory(self, user_id):
        if not self._user_exists(user_id):
            self.glogger.error("The user %s does not exist in the database", user_id)
            return None
        user_session = UserSession()
        user_session.id = user_id
        return user_session

    # ---------------------------------------------
    # Get user-session from the request
    # ----------------------------------------------
    def _get_user_from_request(self, request):
        user_id = self._get_param(request, 'userid')
        if not user_id:
            self.glogger.error("No User-ID. User is not created")
            return None
        password = self._get_param(request, 'password')
        if not password:
            self.glogger.error("No Password. User is not created")
            return None
        user_session = self._get_user_from_memory(user_id)
        if user_session is None:
            return None
        if not self._authenticate(user_id, password):
            self.glogger.error("Incorrect user ID %s or password %s", user_id, password)
            return None
        self._store_userid_object(user_session, user_id)
        self.glogger.info("User ID %s and password %s are OK", user_id, password)
        return user_session

    # ---------------------------------------------
    # Load the user from request
    # ----------------------------------------------
    def _load_from_request(self, request):
        self.glogger.info("_load_from_request is being called")
        user_session = self._get_user_from_request(request)
        return user_session

    # ---------------------------------------------
    # Load the user from request
    # ----------------------------------------------
    def _request_loader(self, request):
        self.glogger.info("_request_loader is being called")
        return self._load_from_request(request)

    # ---------------------------------------------
    # Load the user
    # ----------------------------------------------
    def _load_user(self, user_id):
        self.glogger.info("_load_user is being called")
        return self._get_user_from_memory(user_id)

    # ----------------------------------------------
    # Store object for a userid in the Flask Session
    # ----------------------------------------------
    def _store_userid_object(self, user_object, user_id = None):
        if user_id is None:
            user_id = self.get_current_userid()
        if user_id:
            self.glogger.info("Storing the object in flask for this userid=%s", user_id)
            session[user_id] = user_object
        else:
            self.glogger.info("The userid is None. Cannot store the user object")

    # ----------------------------------------------
    # Clear the userid object from the session
    # ----------------------------------------------
    def _clear_userid_object(self, user_id=None):
        if user_id is None:
            user_id = self.get_current_userid()
        if user_id:
            self.glogger.info("Clearing the stored object in flask for this userid=%s", user_id)
            session.pop(user_id, None)

# ---------------------------------------------
# Load the user session
# Callback functio that is called by flask-login
# ----------------------------------------------
#@glogin_manager.user_loader
#def user_loader(user_id):
#    return sessionmgr_load_user(user_id)

# ---------------------------------------------
# Load the user from request
# Callback functio that is called by flask-login
# ----------------------------------------------
#@glogin_manager.request_loader
#def request_loader(request):
#    return sessionmgr_load_from_request(request)

# ---------------------------------------------
# Unauthorized handler
# Callback functio that is called by flask-login
# ---------------------------------------------
#@glogin_manager.unauthorized_handler
#def unauthorized_handler():
#    return 'Unauthorized'