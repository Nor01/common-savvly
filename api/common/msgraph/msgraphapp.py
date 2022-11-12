from typing import Dict
from typing import List
from typing import Union
import json as json_lib
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from common.util.logging_helper import get_logger
from common.util.config_wrapper import *
#from msgraph.core import GraphClient
import json
import msal
import requests


#-------------------------------------------
# Microsoft Graph Wrapper - Application APIs
#-------------------------------------------
class MsGraphApp:
#    __instance = None
#
#    # ---------------------------------------------
#    # Return the singletone object
#    # ---------------------------------------------
#    @staticmethod
#    def get_instance():  # Static access method.
#        if MsGraphApp.__instance is None:
#            MsGraphApp()
#        return MsGraphApp.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
#        if MsGraphApp.__instance != None:
#            raise Exception("This class (MsGraphApp) is a singleton!")
#            return
#        MsGraphApp.__instance = self
        self.glogger = get_logger("MsGraphApp")
        self.glogger.debug("Creating the MsGraphApp as an application")
        #self.RESOURCE = "https://graph.microsoft.com/"
        #self.api_version = "v1.0"
        #self.account_type = "common"
        #AUTHORITY_URL = "https://login.microsoftonline.com/"
        #AUTH_ENDPOINT = "/oauth2/v2.0/authorize?"
        #TOKEN_ENDPOINT = "/oauth2/v2.0/token"
        #OFFICE365_AUTHORITY_URL = "https://login.live.com"
        #OFFICE365_AUTH_ENDPOINT = "/oauth20_authorize.srf?"
        #OFFICE365_TOKEN_ENDPOINT = "/oauth20_token.srf"
        self._create_msgraph_client()

    # ----------------------------------------------------
    # Create ms-graph-client
    # ---------------------------------------------------
    def _create_msgraph_client(self):
        self.access_token = None
        self.refresh_token = None
        try:
            tenant_id = get_config_string_param("b2c_tenantId")
            client_id = get_config_string_param("b2c_clientId")
            client_secret = get_config_string_param("b2c_clientSecret")
            self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
            scopes = self._get_scopes()
            authority = f"https://login.microsoftonline.com/{tenant_id}"
            self.app_client = msal.ConfidentialClientApplication(
                                client_id=client_id,
                                client_credential=client_secret,
                                authority=authority)
            self.glogger.debug("app_client=%s", self.app_client)
            result = self.app_client.acquire_token_silent(scopes, account=None)
            if not result:
                self.glogger.debug("No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
                result = self.app_client.acquire_token_for_client(scopes=scopes)
            if "access_token" in result:
                self.access_token = result["access_token"]
                self.glogger.debug("Access-token=%s", self.access_token)
            else:
                self.glogger.error("Authentication failed - no access token")
                #print(result)
                return False
            #if "refresh_token" in result:
            #    self.refresh_token = result["refresh_token"]
            #    self.glogger.debug("Refresh-token=%s", self.refresh_token)
            #else:
            #    self.glogger.error("Authentication failed - no refresh token")
            #    print(result)
            #    return False
        except Exception as err:
            self.glogger.error("Exception in creating the MsGraphApp. Err=%s", err)
            return False
        return True

    # ----------------------------------------------------
    # Get scopes
    # ---------------------------------------------------
    def _get_scopes(self):
        graph_url = "https://graph.microsoft.com/"
        self.graph_api_url = f"{graph_url}v1.0/"
        scopes = [f'{graph_url}.default']
        return scopes

    # ----------------------------------------------------
    # Refresh the access token
    # ---------------------------------------------------
    #def _refresh_access_token(self):
    #    if self.app_client is None:
    #        self.glogger.error("No app client exits - cannot refresh token")
    #        return
    #    if self.refresh_token is None:
    #        self.glogger.error("No refresh token exits - cannot refresh it")
    #        return
    #    scopes = self._get_scopes()
    #    result = self.app_client.acquire_token_by_refresh_token(self.refresh_token, scopes=scopes)
    #    if "error" in result:
    #        self.glogger.error("Error in refresh-token. result=%s", result)
    #        return
    #    if "access_token" in result:
    #        self.access_token = result["access_token"]
    #        self.glogger.debug("Access-token=%s", self.access_token)
    #    else:
    #        self.glogger.error("Authentication failed - no access token")
    #        print(result)
    #        return
    #    if "refresh_token" in result:
    #        self.refresh_token = result["refresh_token"]
    #        self.glogger.debug("Refresh-token=%s", self.refresh_token)
    #    else:
    #        self.glogger.error("Authentication failed - no refresh token")
    #        print(result)
    #        return
    #    self.glogger.info("Refresh-token ended successfully. token=%s refresh=%s", self.access_token, self.refresh_token)

    # ----------------------------------------------------
    # Get the list of the users
    # Returns  dict :
    #    If successful, this method returns a 200 OK response code
    #    and collection of user objects in the response body. If a
    #    large user collection is returned, you can use paging in your
    #    app.
    # ---------------------------------------------------
    def get_users_list(self, idx:str = None):
        select = 'id,userName,displayName,mail,givenName,surname,streetAddress,city,postalCode,identities'
        if idx:
            query = f"users/{idx}?$select={select}"
        else:
            query = f"users?$select={select}"

        users_list,retcode = self._make_request(
            method="get",
            endpoint=query
        )
        if not retcode:
            return None

        if "value" in users_list:
            self.glogger.debug("The key value is not found in the returned list: %s", users_list)
            users_list = users_list["value"]
            for user_info in users_list:
                #print(user_info)
                self._fix_email_in_user_info(user_info) # Fix the email in the user-info
        else:
            self._fix_email_in_user_info(users_list)  # Fix the email in the user-info
        #print("get_users_list  ====>")
        #print(users_list)
        return users_list

    # ---------------------------------------------------
    # Get user by id
    # ---------------------------------------------------
    def get_user_by_id(self, userid: str):
        user_list = self.get_users_list(userid)
        if user_list is None:
           self.glogger.error("Failed to get the user info: %s", userid)
           return None
        #if len(user_list) >= 1:
        #    user_list = user_list[0]
        #print("get_user_by_id Result ====>")
        #print(user_list)
        return user_list

    # ----------------------------------------------------
    # Get the list of the users by their IDs
    # ---------------------------------------------------
    def get_users_by_id_list(self, idx_list: list):
        user_list = {}
        for idx in idx_list:
            user_info = self.get_user_by_id(idx)
            if  user_info is None:
                self.glogger.error("Failed to get the user info: %s", idx)
                continue
            user_list[idx] = user_info
        return user_list

    # ---------------------------------------------------
    # Get Email by id
    # ---------------------------------------------------
    def get_email_by_id(self, userid: str):
        result = self.get_user_by_id(userid)
        #print("get_email_by_id result ====>")
        #print(result)
        if not result:
           self.glogger.error("Failed to get the the email of the user:%s", userid)
           return result
        ad_mail = result["mail"]
        if not ad_mail:
           self.glogger.error("Email not found in the returend info from MSGraph.idx=%s result=%s", userid, result)
           return None
        return result["mail"]

    # ---------------------------------------------------
    # Get user ID by email
    # ---------------------------------------------------
    def get_id_by_email(self, email: str):
        email_list = self.get_all_users_email()
        if email_list is None:
            self.glogger.error("Failed to get the list of the emails of all users")
            return None
        #print(email_list)
        for  key,value in email_list.items():
            if value is None:
                continue
            #print(str(key) + " : " + str(value))
            if  value.lower() == email.lower():
                return key
        return None
        #parameters = {"$filter": f"mail eq '{email}'"}
        #result, retcode = self._make_request(
        #    method="get",
        #    endpoint=f"users",
        #    params=parameters
        #             )
        #if not retcode:
        #   self.glogger.error("Failed to get the user by email: %s", email)
        #   return None
        #if not "value" in result:
        #    self.glogger.error("Expected to find value in the response: %s", result)
        #    return None
        #print(result)
        ##val_list = result["value"]
        ##if len(val_list) > 1:
        ##    self.glogger.error("There are too many users with the email=%s: %d", email, len(val_list))
        ##    return None
        #userinfo = result["value"]
        #print(userinfo)
        #return userinfo["id"]

    # ---------------------------------------------------
    # Create a user
    # ---------------------------------------------------
    def create_new_user(self, firstname: str, lastname:str, email:str):
        #username = firstname + "." + lastname + "@" + config_get_b2c_domain_name()
        userinfo = {
            "accountEnabled": True,
            "mail" : email,
            "displayName": firstname + " " + lastname,
            "givenName": firstname,
            "surname": lastname,
            #"mailNickname": firstname + "_" + lastname, # This must be out
            #"userPrincipalName": "Unknown",             # This must be out
            "passwordProfile": {
                "forceChangePasswordNextSignIn": False,  # This must be False
                "password": config_get_b2c_new_user_default_password()
                                },
            "identities" : [
                    {
                    "SignInType" : "emailAddress",
                    "Issuer" : config_get_b2c_domain_name(),
                    "IssuerAssignedId" : email
                    }
                ]
            }
        result,retcode = self._make_request(
            method="post",
            endpoint=f'users',
            json=userinfo
        )
        if not retcode:
           self.glogger.error("Failed to add a new user to AAD: name=%s last=%s email=%s", firstname, lastname, email)
           return None
        return result

    # ---------------------------------------------------
    # Update 'address' of the user
    # ---------------------------------------------------
    def update_user_address(self, userid: str, street:str, city:str, postalcode:str, country:str = None):
        userinfo = {"city": city,
                    "streetAddress": street,
                    "postalCode": postalcode,
                    "country": country}
        result, retcode = self._make_request(
            method="patch",
            endpoint=f'users/{userid}',
            json=userinfo
        )
        if not retcode:
            self.glogger.error("Failed to update user address street=%s city=%s zip=%s country=%s to the user:%s", street, city, postalcode, country, userid)
            return None
        return result

    # -------------------------------------------------------
    # Get the emails of all users (as dictionary)
    # -------------------------------------------------------
    def get_all_users_email(self):
        user_list = self.get_users_list()
        if not user_list:
            return None
        #print(users_info)
        #try:
        #    user_list = users_info["value"]
        #except Exception as err:
        #    self.glogger.error("Exception in getting users List. Err=%s", err)
        #    return None
        try:
            email_list = {}
            for user in user_list:
                #print(user)
                #self.glogger.info("id=%s mail=%s", user["id"], user["mail"])
                email_list[user["id"]] = user["mail"]
        except Exception as err:
            self.glogger.error("Exception in parsing the users info. Err=%s", err)
            return None
        return email_list

    # ----------------------------------------------------
    # Delete a user
    # ---------------------------------------------------
    def delete_user(self, idx:str):
        result,retcode = self._make_request(
            method="delete",
            endpoint=f"users/{idx}"
        )
        if not retcode:
            self.glogger.error("Failed to delete user idx from AAD:%s", idx)
            return None
        return result

    # ----------------------------------------------------
    # Reset User's password
    # The parameter can be either ID or email
    # ---------------------------------------------------
    def reset_password(self, idx_email:str):
        passwordprofile = {
            "passwordProfile": {
                "forceChangePasswordNextSignIn": False,  # This must be False
                "password": config_get_b2c_new_user_default_password()
                                }
                    }
        result, retcode = self._make_request(
            method="patch",
            endpoint=f"users/{idx_email}",
            json=passwordprofile
        )
        if not retcode:
            self.glogger.error("Failed to reset password idx:%s", idx)
            return None
        return result

    # ---------------------------------------------------
    # Send an email
    # ---------------------------------------------------
    #def send_email(self, idx: str, email: str, subject:str, body:str):
    #    return self.send_email_to_list(idx, [email], subject, body)
#
    # ---------------------------------------------------
    # Send an email to a list of Recipients
    # ---------------------------------------------------
    #def send_email_to_list(self, idx: str, email_list: list, subject:str, body:str):
    #    recipients_email_list = self._create_recipients_email_list(email_list)
    #    if len(recipients_email_list) < 1:
    #        self.glogger.error("The list of the email recipients is empty")
    #        return
    #    email_properties = {
    #        "message": {
    #            "subject": subject,
    #            "body": {
    #                "contentType": "Text",
    #                "content": body
    #            },
    #            "toRecipients": recipients_email_list,
    #        },
    #        "saveToSentItems": "false"
    #    }
    #    result, retcode = self._make_request(
    #        method="post",
    #        endpoint=f"users/{idx}/sendMail",
    #        json = email_properties
    #    )
    #    if not retcode:
    #        self.glogger.error("Failed to reset password idx:%s", idx)
    #        return None
    #    return result

    # ---------------------------------------------------
    # Create a list of emails
    # ---------------------------------------------------
    #def _create_recipients_email_list(self, email_list : list):
    #    recipients_email_list = []
    #    for email in email_list:
    #        recipient = { "emailAddress": {"address": email}}
    #        recipients_email_list.append(recipient)
    #    return recipients_email_list

    # ---------------------------------------------------
    # Update 'Other Emails' of the user
    # ---------------------------------------------------
    #def _update_user_email(self, userid: str, email:str):
    #    userinfo = {"otherMails": [email]}
    #    result, retcode = self._make_request(
    #        method="patch",
    #        endpoint=f'users/{userid}',
    #        json=userinfo
    #    )
    #    if not retcode:
    #       self.glogger.error("Failed to add email %s to the user:%s", email, userid)
    #       return None
    #    return result

    # --------------------------------------------------------------------------
    # find and set the user email in the retreived info
    # ---------------------------------------------------------------------------
    def _fix_email_in_user_info(self, user_info: dict = None) -> dict:
        if "mail" in user_info and user_info["mail"] is not None:
            self.glogger.debug("This user has already a valid email:%s", user_info)
            return user_info
        if not "identities" in user_info:
            self.glogger.error("Could not find identities in the user info: %s", user_info)
            return user_info
        identities = user_info["identities"]
        for identity in identities:
            if not "signInType" in identity:
                self.glogger.error("Could not find signInType in the identity: %s", identity)
                continue
            if not identity["signInType"] == "emailAddress":
                self.glogger.debug("signInType is not emailAddress; skipping. identity: %s", identity)
                continue
            user_info["mail"] = identity["issuerAssignedId"]
            break
        #print(user_info)
        return user_info

    # --------------------------------------------------------------------------
    # Build a header for the request
    # Parameters :  additional_args : dict (optional, Default=None)
    #             Any additional headers that need to be sent in the
    #             request.
    #
    # Returns:       dict :
    # ---------------------------------------------------------------------------
    def _build_headers(self, additional_args: dict = None) -> Dict:
        headers = {"Authorization": f"Bearer {self.access_token}"}
        if additional_args:
            headers.update(additional_args)
        self.glogger.debug("headers=%s", headers)
        return headers

    # --------------------------------------------------------------------------
    # Build the URL used the make string.
    # Parameters :  endpoint : str
    #             The endpoint used to make the full URL.
    # Returns:    str:
    #             The full URL with the endpoint needed.
    # ---------------------------------------------------------------------------
    def _build_url(self, endpoint: str) -> str:
        url = self.graph_api_url + endpoint
        self.glogger.debug("url=%s", url)
        return url

    # --------------------------------------------------------------------------
    # Handles all the requests in the library.
    # A central function used to handle all the requests made in the library,
    #         this function handles building the URL, defining Content-Type, passing
    #         through payloads, and handling any errors that may arise during the request.
    # Parameters :  method : str
    #             The Request method, can be one of the
    #             following: ["get","post","put","delete","patch"]
    #         endpoint : str
    #             The API URL endpoint, example is "quotes"
    #         params : dict (optional, Default=None)
    #             The URL params for the request.
    #         data : dict (optional, Default=None)
    #             A data payload for a request.
    #         json : dict (optional, Default=None)
    #             A json data payload for a request
    #         expect_no_response: bool (optional, Default=False)
    #             Some responses will only return a status code,
    #             so if this is set to True it will only return
    #             the status code.
    # Returns:    Union[List, Dict]:
    #             The resource object or objects.
    # ---------------------------------------------------------------------------
    def _make_request(self,
               method: str,
               endpoint: str,
               params: dict = None,
               data: dict = None,
               json: dict = None,
               additional_headers: dict = None,
               expect_no_response: bool = False
           ) -> Union[Dict, List]:
       url = self._build_url(endpoint=endpoint)
       self.glogger.debug("url=%s", url)
       headers = self._build_headers(additional_args=additional_headers)
       request_session = requests.Session()
       request_session.verify = True
       request_request = requests.Request(
                       method=method.upper(),
                       headers=headers,
                       url=url,
                       params=params,
                       data=data,
                       json=json
                   ).prepare()
       response: requests.Response = request_session.send(request=request_request)
       request_session.close()
       # If it"s okay and no details.
       result = None
       retcode = False
       if response.ok and expect_no_response:
           self.glogger.debug("Response: OK")
           result =  {"status_code": response.status_code}
           retcode = True
       elif response.ok and len(response.content) > 0:
           self.glogger.debug("Response: OK. dataLen = %d", len(response.content))
           result = response.json()
           self.glogger.debug("result=%s", result)
           retcode= True
       elif len(response.content) == 0 and response.ok:
           self.glogger.debug("Request was successful. But no data returned")
           result = {
               "message": "Request was successful, status code provided.",
               "status_code": response.status_code
           }
           retcode = True
       elif not response.ok:
           self.glogger.error("Request Failed")
           result = {
               "error_code": response.status_code,
               "response_url": response.url,
               "response_body": json_lib.loads(response.content.decode("ascii")),
               "response_request": dict(response.request.headers),
               "response_method": response.request.method,
           }
           self.glogger.error(msg=json_lib.dumps(obj=result, indent=4))
           retcode = False
           #raise requests.HTTPError()
       return result, retcode


# ---------------------------------------------------------------------------
# Refresh the access token
# ---------------------------------------------------------------------------
#def msgraphapp_refresh_token():   return MsGraphApp.get_instance()._refresh_access_token()
