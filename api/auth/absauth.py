import re
from common.util.logging_helper import get_logger
from flask import Flask, request, redirect, session, url_for
from common.util.config_wrapper import get_config_string_param
from proxy.session import *

# -------------------------------------------------------------------------------------------------
# Class AbsAuth - Abstract Auth
# -------------------------------------------------------------------------------------------------
class AbsAuth():
    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, app):
        self.glogger = get_logger()
        self.app     = app


    # -------------------------------------------------------
    # Must be implemented by the child
    # Returns:
    #  redirect_url : URL to forward to do the authentication
    # -------------------------------------------------------
    def _get_user_flow_url(self, user_flow=None):
        self.glogger.error("This function must be implemented by the child")
        return None

    # -------------------------------------------------------
    # Get a specific user flow url and store in the session
    #-------------------------------------------------------
    def _get_specific_user_flow_url_store(self, user_flow=None):
        session_set_user_flow(user_flow)
        url = self._get_user_flow_url(user_flow)
        self.glogger.info("URL for flow=%s:  %s", user_flow, url)
        return url

    # -------------------------------------------------------
    # Get a specific user flow url: Login
    # Get a specific user flow url: Register User
    # Get a specific user flow url: Register Advisor
    #-------------------------------------------------------
    def get_login_url(self): return self._get_specific_user_flow_url_store(self._get_signin_flow())
    def get_register_user_url(self): return self._get_specific_user_flow_url_store(self._get_signup_user_flow())
    def get_register_advisor_url(self): return self._get_specific_user_flow_url_store(self._get_signup_ria_flow())

    # -------------------------------------------------------
    # Must be implemented by the child
    # -------------------------------------------------------
    def check_result(self, flow=None):
        self.glogger.error("This function must be implemented by the child")
        return False

    # -------------------------------------------------------
    # Must be implemented by the child
    # -------------------------------------------------------
    def post_logout(self):
        self.glogger.error("This function must be implemented by the child")

    # -------------------------------------------------------
    # Must be implemented by the child
    # -------------------------------------------------------
    def get_current_userid(self):
        self.glogger.error("This function must be implemented by the child")
        return None

    # -------------------------------------------------------
    # Get logout API
    # -------------------------------------------------------
    def get_logout_api(self):
        return "logout"

    # -------------------------------------------------------
    # Get Callback API for Authorized
    # -------------------------------------------------------
    def get_authorized_api(self):
        return get_config_string_param("b2c_redirectPath")

    # -------------------------------------------------------
    # Get Callback URI for Authorized
    # -------------------------------------------------------
    def get_authorized_uri(self):
        url = url_for(self.get_authorized_api(), _external=True)
        self.glogger.error("url=%s", url)
        return url

    # ------------------------------------------------------
    # Parse Access Token
    # ------------------------------------------------------
    def parse_access_token(self):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not self._is_valid_auth_header(auth_header):
                self.glogger.error("The Token not found in the header: %s", auth_header)
                return None
            jwt_token = auth_header[7:]  # Throw out 'Bearer '
            parsed_token = self._parse_access_token(jwt_token)
            if parsed_token is None:
                self.glogger.error("Failed to parse the token. Probably expoired: %s", jwt_token)
        except Exception as err:
            self.glogger.error("Failed to parse token. Probably Expired. err=%s", err)
            return None
        self.glogger.debug("Parsed Access Token=%s", parsed_token)
        return parsed_token

    # -------------------------------------------------------
    # Must be implemented by the child
    # -------------------------------------------------------
    def _parse_access_token(self, jwt_token):
        self.glogger.error("This function must be implemented by the child")
        return None

    # ------------------------------------------------------
    # Checks if an ``Authorization`` header follows
    # the format "Bearer [token]" (not case sensitive)
    # ------------------------------------------------------
    def _is_valid_auth_header(self, auth_header: str) -> bool:
        AUTH_HEADER_RE = re.compile(r"^Bearer {1}\S*$", re.IGNORECASE)
        return bool(AUTH_HEADER_RE.match(auth_header))

    # -----------------------------------------------------------------------------------------
    # Get a parameter from the request
    # -----------------------------------------------------------------------------------------
    def _get_param(self, request, param_name):
        if not request.args:
            self.glogger.error("MissingParamater. Expected parameter: %s", param_name)
            return None
        value = request.args.get(param_name)
        if not value:
            self.glogger.error("BadParamaterr. Expected %s", param_name)
            return None
        self.glogger.debug("%s=%s", param_name, value)
        return value

    # ------------------------------------------------------
    # Configuration parameters
    # ------------------------------------------------------
    def _get_signinup_user_flow(self):     return get_config_string_param("b2c_signupsignin_user_flow")
    def _get_signup_ria_flow(self):        return get_config_string_param("b2c_signup_ria_flow")
    def _get_signup_user_flow(self):       return get_config_string_param("b2c_signup_user_flow")
    def _get_signin_flow(self):            return get_config_string_param("b2c_signin_flow")