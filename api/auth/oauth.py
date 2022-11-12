import os
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from common.util.logging_helper import get_logger
from auth.absauth import *

# -------------------------------------------------------------------------------------------------
# Class Oauth
# Taken from here:
# https://github.com/requests/requests-oauthlib/blob/master/docs/examples/real_world_example.rst
# -------------------------------------------------------------------------------------------------
class Oauth(AbsAuth):
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance(app):  # Static access method.
        if Oauth.__instance is None:
            Oauth(app)
        return Oauth.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, app):
        if Oauth.__instance != None:
            raise Exception("This class is a singleton!")
            return
        super().__init__(app)
        Oauth.__instance = self
        self.glogger = get_logger()
        self.glogger.info("Creating the instance of Oauth")

        # This allows us to use a plain HTTP callback
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

        # This information is obtained upon registration of a new GitHub OAuth
        # application here: https://github.com/settings/applications/new
        #self.client_id = "369b9d2cac53a7da34b9"
        #self.client_secret = "812ccd078333204e104cb7bdbcbcc536ffab4991"
        #self.authorization_base_url = 'https://github.com/login/oauth/authorize'
        #self.token_url = 'https://github.com/login/oauth/access_token'
        #self.redirect_uri = 'http://localhost:5000/authorized'
        #self.callback_uri = url_for("authorized", _external=True)

    # -------------------------------------------------------
    # Redirect to the server (OAuth provider (i.e. Github)
    # Must be implemented by the child
    # Returns:
    #  redirect_url : URL to forward to do the authentication
    # -------------------------------------------------------
    def _get_user_flow_url(self, flow=None):
        #if self.get_current_userid():
        #    return True, None
        try:
            # Step 1: User Authorization.
            # Redirect the user/resource owner to the OAuth provider (i.e. Github)
            # using an URL with a few key OAuth parameters.
            server = OAuth2Session(self._get_client_id(), redirect_uri=self.get_authorized_uri())
            authorization_url, state = server.authorization_url(self._get_authority_template())
            self.glogger.info("authorization_url=%s", authorization_url)
            self.glogger.info("state=%s", state)
            # State is used to prevent CSRF, keep this for later.
            session['oauth_state'] = state
            return authorization_url
        except Exception as err:
            self.glogger.error("Ouath authenticate() got exception. err=%s", err)
        return None
        # Step 2: User authorization, this happens on the provider.

    # ---------------------------------------------------------------------
    # The callback function calls this function after user authorization
    # ----------------------------------------------------------------------
    def check_result(self, flow=None):
        self.glogger.debug("The function check_result() is called after authorization")
        self._check_session_state()
        #if not self._check_session_state():
        #    return False
        try:
            # Step 3: Retrieving an access token.
            # The user has been redirected back from the provider to your registered
            # callback URL. With this redirection comes an authorization code included
            # in the redirect URL. We will use that to obtain an access token.
            server = OAuth2Session(self.client_id, state=session['oauth_state'])
            self.glogger.info("request.url=%s", request.url)
            token = server.fetch_token(self._get_token_url(),
                                       client_secret=self._get_client_secret(),
                                       authorization_response=request.url)
            # At this point you can fetch protected resources but lets save
            # the token and show how this is done from a persisted token
            # in /profile.
            #request.session['token'] = token
            session['oauth_token'] = token
            self.glogger.info("Token=%s", token)
            return True
        except Exception as err:  # Usually caused by CSRF
            self.glogger.error("Ouath callback fetch_token() got exception. err=%s", err)
            return True # Request is not passed - TBD
        return False

    # -----------------------------------
    # Get the current logged-in user
    # -----------------------------------
    def get_current_userid(self):
        self.glogger.error("Ouath: This function is not implemented yet: get_current_userid()")
        return None

    # ---------------------------------
    # Check state
    # ---------------------------------
    def _check_session_state(self):
        self.glogger.info("request.url=%s", request.url)
        #self.glogger.info("request.session['token']=%s", request.session['token'])
        #print(request.values)
        #print(request.view_args)
        #code = request.args.get('code')
        req_state = request.args.get('state')
        ses_state = session.get("oauth_state")
        self.glogger.info("ReqState=%s SessState=%s", req_state, ses_state)
        if req_state != ses_state:
            self.glogger.error("The state is not as expected. ReqState=%s SessState=%s", req_state, ses_state)
            return True   # Login Canceled - Do to a bug !!!!  TBD
            return False   # Login Canceled
        return True

    # ------------------------------------------------------
    # Configuration parameters
    # ------------------------------------------------------
    def _get_client_id(self):              return "369b9d2cac53a7da34b9"
    def _get_client_secret(self):          return "812ccd078333204e104cb7bdbcbcc536ffab4991"
    def _get_authority_template(self):     return "https://github.com/login/oauth/authorize"
    def _get_token_url(self):              return "https://github.com/login/oauth/access_token"
