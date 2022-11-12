import os
import msal
#from flask import Flask, request, redirect, session, url_for
from common.util.logging_helper import get_logger
from auth.absauth import *
from common.util.config_wrapper import get_config_string_param
from proxy.session import *
from proxy.request_helper import *
from azure_ad_verify_token import verify_jwt

# -------------------------------------------------------------------------------------------------
# Class ActiveDir
# Taken from here:
# https://github.com/Azure-Samples/ms-identity-python-webapp/blob/master/app.py
# https://docs.microsoft.com/en-us/azure/active-directory-b2c/configure-authentication-sample-python-web-app
# https://blogs.aaddevsup.xyz/2019/07/understanding-the-difference-between-application-and-delegated-permissions-from-oauth2-authentication-flows-perspective/
# https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow
# https://docs.microsoft.com/en-us/azure/active-directory/develop/sample-v2-code
# -------------------------------------------------------------------------------------------------
class ActiveDir(AbsAuth):
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance(app):  # Static access method.
        if ActiveDir.__instance is None:
            ActiveDir(app)
        return ActiveDir.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, app):
        if ActiveDir.__instance != None:
            raise Exception("This class is a singleton!")
            return
        super().__init__(app)
        ActiveDir.__instance = self
        self.glogger = get_logger()
        self.glogger.debug("Creating the instance of ActiveDir")
        #app.jinja_env.globals.update(_build_auth_code_flow=self._build_auth_code_flow)  # Used in template
        #app.jinja_env.globals.update(_build_auth_url=self._build_auth_url)  # Used in template

    # -------------------------------------------------------
    # Redirect to the server (to authenticate)
    # Must be implemented by the child
    # Returns:
    #  redirect_url : URL to forward to do the authentication
    # -------------------------------------------------------
    def _get_user_flow_url(self, user_flow=None):
        self.glogger.debug("user_flow:%s", user_flow)
        try:
            auth_url = self._build_auth_url(scopes=self._get_msal_scope(), user_flow=user_flow)
            session["flow"] = auth_url
            self.glogger.debug("flow:%s", auth_url)
            self.glogger.debug("Login redirect=%s", auth_url)
        except Exception as err:
            self.glogger.error("Activedir authenticate() got exception. err=%s", err)
            return None
        return auth_url

    # ---------------------------------------------------------------------------------
    # Authenticate Call back function (with or without MFA)
    # ---------------------------------------------------------------------------------
    def check_result(self, user_flow=None):
        if user_flow is None: user_flow = session_get_user_flow()
        self.glogger.debug("Callback is being called. flow=%s", session.get("flow"))
        self.glogger.debug("Callback request.args=%s", request.args)
        try:
            cache = self._load_cache()
            self.glogger.debug("The function check_result() is called after authorization")
            if not session_check_state():
                self.glogger.error("check_result: sessionCheckState returned False")
                # return False
            if request_check_is_error():
                self.glogger.error("check_result: requestCheckIsError returned True")
                # return False
            code = request.args.get('code')
            if not code:
                self.glogger.error("No Code found in the request")
                #return False
            self.glogger.debug("Calling _build_msal_app_obj()")
            msalobj = self._build_msal_app_obj(cache=cache, user_flow=user_flow)
            self.glogger.debug("Accuiring Token by Auth Code....")
            result = msalobj.acquire_token_by_authorization_code(code=code,
                                                                 scopes=self._get_msal_scope(),
                                                                 redirect_uri=self._build_callback_url(self.get_authorized_api()))
            if "error" in result:
                self.glogger.error("Error returned in result: %s", result)
                return False
            self.glogger.debug("result: %s", result)
            session_set_user_info(result.get("id_token_claims"))
            session_set_access_token(result.get("access_token"))
            session_set_refresh_token(result.get("refresh_token"))
            self._save_cache(cache)
            return True
        except ValueError:  # Usually caused by CSRF
            self.glogger.error("Callback got exception of ValueError. Ignoring...")
            pass  # Simply ignore them
        except Exception as err:
            self.glogger.error("Callback got an exception err=%s", err)
            pass  # Simply ignore them
        return True

    # ---------------------------------------------
    # Cleanup during logout
    # ---------------------------------------------
    def post_logout(self):
        session_print()
        if session_get_user_id() is None:
            self.glogger.error("No User is logged in - cannot logout")
            #return
        session_clear_cache()
        session_clear_user()  # Wipe out user and its token cache from session
        user_flow = self._get_signin_flow()
        url = self._get_msal_authority(user_flow) + "/oauth2/v2.0/logout?post_logout_redirect_uri=" + url_for(self.get_logout_api(), _external=True)
        self.glogger.debug("logout url=%s", url)
        return redirect(url)

    # -----------------------------------
    # Get the current logged-in user
    # -----------------------------------
    def get_current_userid(self):
        return session_get_user_id()

    # ---------------------------------------------------------------------------
    # Get the MSAL parameter: client authority
    # ---------------------------------------------------------------------------
    def _get_msal_authority(self, user_flow):
        #user_flow = session_get_user_flow()
        template = self._get_authority_template()
        #authority = template.format(tenant=self._get_tenant_name(), user_flow=self._get_signinup_user_flow())
        authority = template.format(tenant=self._get_tenant_name(), user_flow=user_flow)
        self.glogger.debug("authority=%s", authority)
        return authority

    # ---------------------------------------------------------------------------
    # Get the MSAL scope as a list
    # ---------------------------------------------------------------------------
    def _get_msal_scope(self):
        b2cscope_arr = self._get_scope_template()
        self.glogger.debug("b2cscope_arr=%s", b2cscope_arr)
        for inx in range(len(b2cscope_arr)):
            template = b2cscope_arr[inx]
            self.glogger.debug("template=%s", template)
            scope = template.format(tenant=self._get_tenant_name())
            self.glogger.debug("scope=%s", scope)
            b2cscope_arr[inx] = scope
        self.glogger.debug("b2cscope_arr=%s", b2cscope_arr)
        return b2cscope_arr

    # ----------------------------------------------
    # Build the full URL of the callback API
    # ----------------------------------------------
    def _build_callback_url(self, callbakapi):
        #callbakapi = self.get_authorized_api()
        cb_url = url_for(callbakapi, _external=True)
        self.glogger.debug("Before updating the URL: " + cb_url)
        cb_url = cb_url.replace(self._get_app_service_name(), self._get_dns_name())
        if not 'localhost' in cb_url:
            cb_url = cb_url.replace('http%3A%2F%2F', 'https%3A%2F%2F')  # Oh yeah, add the port to the URL!
            cb_url = cb_url.replace('http:', 'https:')  # Oh yeah, add the port to the URL!
            cb_url = cb_url.replace(':80', '')  # Remove port=80
        self.glogger.debug("The Callback URL is: %s", cb_url)
        return cb_url

    # ---------------------------------------------
    # Get the tokenn
    # ---------------------------------------------
    def _get_token(self, user_flow=None):
        scope = self._get_msal_scope()
        token = self._get_token_from_cache(scope, user_flow=user_flow)
        if not token:
            self.glogger.error("No Token found. The user is not logged in")
            return None
        token = token['access_token']
        self.glogger.debug("The token is: %s", token)
        return  token

    # ---------------------------------------------
    # Load the Cache
    # ---------------------------------------------
    def _load_cache(self):
        return None # No Cache
        cache = msal.SerializableTokenCache()
        if session_get_cache():
            cache.deserialize(session_get_cache())
        return cache

    # ---------------------------------------------
    # Save the Cache
    # ---------------------------------------------
    def _save_cache(self, cache):
        return  # No Cache
        if cache.has_state_changed:
            session_set_cache(cache.serialize())

    # ---------------------------------------------
    # Build MSAL Client Application Object (Class)
    # ---------------------------------------------
    def _build_msal_app_obj(self, cache=None, authority=None, user_flow=None):
        msalobj = msal.ConfidentialClientApplication(self._get_msal_client_id(),
                                                     client_credential= self._get_msal_client_secret(),
                                                     authority=authority or self._get_msal_authority(user_flow),
                                                     token_cache=cache)
        self.glogger.debug("result=%s", msalobj)
        return msalobj

    # ----------------------------------------------
    # Build url to authorization code flow
    # ------------------------------p----------------
    def _build_auth_url(self, authority=None, scopes=None, user_flow=None):
        redirect = self._build_callback_url(self.get_authorized_api())
        self.glogger.debug("The redirect URL is: %s", redirect)
        msalobj = self._build_msal_app_obj(authority=authority, user_flow=user_flow)
        session_set_random_state()
        self.glogger.debug("Authenticating as an administrator")
        auth_url = msalobj.get_authorization_request_url(scopes=scopes or [],
                                                         redirect_uri=redirect,
                                                         state=session_get_random_state())
        self.glogger.debug("AuthUrl=%s", auth_url)
        return auth_url

    # ------------------------------------------
    # Retrieve a token from token cache
    # ------------------------------------------
    def _get_token_from_cache(self, scope=None, user_flow=None):
        cache = self._load_cache()  # This web app maintains one cache per session
        msalobj = self._build_msal_app_obj(cache=cache, user_flow=user_flow)
        accounts = msalobj.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            self.glogger.debug("There are %d accounts in msal", len(accounts))
            result = msalobj.acquire_token_silent(scope, account=accounts[0])
            self._save_cache(cache)
            return result
        self.glogger.info("The are no accounts in MSAL")

    # ------------------------------------------------------
    # Parse Access Token
    # ------------------------------------------------------
    def _parse_access_token(self, accessToken):
        azure_ad_issuer_template = self._get_ad_issuer_template()
        azure_ad_issuer = azure_ad_issuer_template.format(tenant=self._get_tenant_name(), tenantid=self._get_tenant_id())
        self.glogger.debug("azure_ad_issuer=%s", azure_ad_issuer)

        azure_ad_jwks_uri_template = self._get_ad_jwks_uri_template()
        azure_ad_jwks_uri = azure_ad_jwks_uri_template.format(tenant=self._get_tenant_name())
        self.glogger.debug("azure_ad_jwks_uri=%s", azure_ad_jwks_uri)

        payload = verify_jwt(
            token=accessToken,
            valid_audiences=[self._get_msal_client_id()],
            issuer=azure_ad_issuer,
            jwks_uri=azure_ad_jwks_uri,
            verify=True)
        if payload is None:
            return None
        if not "oid" in payload:
            self.glogger.error("Expected to find oid in the Token, but not found: %s", payload)
            return None
        if not "given_name" in payload:
            self.glogger.info("Expected to find given_name in the Token, but not found: %s", payload)
            #return None
        if not "family_name" in payload:
            self.glogger.info("Expected to find family_name in the Token, but not found: %s", payload)
            #return None
        if not "state" in payload:
            self.glogger.info("Expected to find state in the Token, but not found: %s", payload)
            #return None
        if not "extension_crd_number" in payload:   # Individual CRD number
            self.glogger.info("Expected to find extension_crd_number in the Token, but not found: %s", payload)
            #return None
        if not "extension_PhoneNumber" in payload:
            self.glogger.info("Expected to find extension_PhoneNumber in the Token, but not found: %s", payload)
            #return None
        if not "extension_company_crd_number" in payload:
            self.glogger.info("Expected to find extension_company_crd_number in the Token, but not found: %s", payload)
            #return None
        if not "extension_company_name" in payload:
            self.glogger.info("Expected to find extension_company_name in the Token, but not found: %s", payload)
            #return None
        if not "emails" in payload:
            self.glogger.error("Expected to find emails in the Token, but not found: %s", payload)
            return None
        session_set_user_info(payload)
        return payload

    # ------------------------------------------------------
    # Configuration parameters
    # ------------------------------------------------------
    def _get_dns_name(self):               return get_config_string_param("dns_name")
    def _get_app_service_name(self):       return get_config_string_param("app_service_name")
    def _get_msal_client_id(self):         return get_config_string_param("b2c_clientId")
    def _get_msal_client_secret(self):     return get_config_string_param("b2c_clientSecret")
    def _get_authority_template(self):     return get_config_string_param("b2c_authority_template")
    def _get_scope_template(self):         return get_config_string_param("b2c_scope_template")
    def _get_tenant_name(self):            return get_config_string_param("b2c_tenantName")
    def _get_tenant_id(self):              return get_config_string_param("b2c_tenantId")
    def _get_ad_issuer_template(self):     return get_config_string_param("b2c_ad_issuer_template")
    def _get_ad_jwks_uri_template(self):   return get_config_string_param("b2c_ad_jwks_uri_template")


