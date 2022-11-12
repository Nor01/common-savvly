#from azure.graphrbac import GraphRbacManagementClient
#from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from common.util.logging_helper import get_logger
from common.util.config_wrapper import get_config_string_param
from msgraph.core import GraphClient




###    #-------------------------------------------
###    # Active Directory Wrapper
###    #-------------------------------------------
###    class AzureADWrapper:
###        __instance = None
###        auth_as_app = "AsApp"
###        auth_as_user = "AsUser"
###
###        # ---------------------------------------------
###        # Return the singletone object
###        # ---------------------------------------------
###        @staticmethod
###        def get_instance():  # Static access method.
###            if AzureADWrapper.__instance is None:
###                AzureADWrapper()
###            return AzureADWrapper.__instance
###
###        # ---------------------------------------------
###        # Constructor
###        # ---------------------------------------------
###        def __init__(self, auth_mode : str = "AsApp"):
###            if AzureADWrapper.__instance != None:
###                raise Exception("This class (AzureADWrapper) is a singleton!")
###                return
###            AzureADWrapper.__instance = self
###            try:
###                self.glogger = get_logger("aadwrap")
###
###                if auth_mode == AzureADWrapper.auth_as_user:
###
###                else:
###
###
###
###
###
###
###                return
###
###
###                subscription_id = get_config_string_param('b2c_subscriptionId')
###                tenant_id = get_config_string_param("b2c_tenantId")
###                client_id = get_config_string_param("b2c_clientId")
###                client_secret = get_config_string_param("b2c_clientSecret")
###                resource = get_config_string_param("b2c_microsoft_graph_recource")
###                credentials = ServicePrincipalCredentials(
###                        client_id=client_id,
###                        secret=client_secret,
###                        tenant=tenant_id,
###                        resource=resource)
###                self.graphrbac_client = GraphRbacManagementClient(credentials, tenant_id)
###                if self.graphrbac_client is None:
###                    raise Exception("Got an exception when tried to creat AAD Graph Management")
###            except Exception as err:
###                self.glogger.error("Exception in creating the ActiveDirWrapper. Err=%s", err)
###
###
###
###
###
###
###
###        # ----------------------------------------------------
###        # Get the application list
###        # ---------------------------------------------------
###        def get_application_list(self) -> list:
###            applist = []
###            try:
###                apps  = self.graphrbac_client.applications.list()
###                for app in apps:
###                   self.glogger.info("app: %s", app)
###                   applist.append(app)
###            except Exception as err:
###                self.glogger.error("Exception while trying to get the application list from AAD. Err=%s", err)
###                return None
###            return applist
###
###        # ----------------------------------------------------
###        # Get the info for all users
###        # ---------------------------------------------------
###        def get_all_users_info(self) -> dict:
###            userlist = {}
###            try:
###                users = self.graphrbac_client.users.list()
###                for user in users:
###                    userdata = self._get_user_info(user)
###                    userlist[user.object_id] = userdata
###                    self.glogger.info("UserInfo: %s", userdata)
###            except Exception as err:
###                self.glogger.error("Exception while trying to get the user list from AAD. Err=%s", err)
###                return None
###            return userlist
###
###        # ----------------------------------------
###        # Get the emails of all users (as dictionary)
###        # ----------------------------------------
###        def get_all_users_email(self) -> dict:
###            users_info = self.get_all_users_info()
###            if not users_info:
###                return None
###            email_list = {}
###            for userid, userdata in users_info.items():
###                self.glogger.info("id=%s email=%s", userid, userdata["email"])
###                email_list[userid] = userdata["email"]
###            return email_list
###
###        # ----------------------------------------------------
###        # Get the info for a user by its id
###        # ---------------------------------------------------
###        def get_user_info_by_id(self, user_id: str) -> dict:
###            userlist = self.get_all_users_info()
###            for userid, userdata in userlist.items():
###                # self.glogger.debug("id=%s userdata=%s", userid, userdata)
###                if userdata["userid"] == user_id:
###                    self.glogger.info("UserInfoByID: id=%s - %s", user_id, userdata)
###                    return userdata
###            self.glogger.error("Failed to find the user info of this id=%d", user_id)
###            return None
###
###        # ----------------------------------------------------
###        # Get the info for a user by its emai
###        # ---------------------------------------------------
###        def get_user_info_by_email(self, email: str) -> dict:
###            user_id = self.get_user_id_by_email(email)
###            if not user_id:
###                return None
###            return self.get_user_info_by_id(user_id)
###
###        # ---------------------------------------------------
###        # Get the email by id
###        # ---------------------------------------------------
###        def get_user_email_by_id(self, userid: str) -> str:
###            userinfo = self.get_user_info_by_id(userid)
###            if not userinfo:
###                self.glogger.error("Failed to get the ID of this user=%s in the AD", userid)
###                return None
###            self.glogger.info("userid=%s userinfo=%s", userid, userinfo)
###            return userinfo["email"]
###
###        # ---------------------------------------------------
###        # Get the ID of the user
###        # ---------------------------------------------------
###        def get_user_id_by_email(self, email: str) -> str:
###            email = email.lower()
###            users = self.graphrbac_client.users.list()
###            for user in users:
###                curemail = self._get_user_email_by_id(user)
###                if email == curemail:
###                    return user.object_id
###            self.glogger.error("Failed to find the ID of this email=%s in the AD", email)
###            return None
###
###        # ---------------------------------------------------
###        # Check if User exists (by ID)
###        # ---------------------------------------------------
###        def user_exists_by_id(self, userid: str) -> bool:
###            if self.get_user_info_by_id(userid):
###                return True
###            return False
###
###        # ---------------------------------------------------
###        # Check if User exists (by email))
###        # ---------------------------------------------------
###        def user_exists_by_email(self, email: str) -> bool:
###            if self.get_user_id_by_email(email):
###                return True
###            return False
###
###        # ----------------------------------------------------
###        # Delete User from AD (by ID)
###        # ---------------------------------------------------
###        def delete_user_by_id(self, user_id: str):
###            try:
###                self.glogger.info("Deleting the user=%s from Active Directory", user_id)
###                self.graphrbac_client.users.delete(user_id)
###            except Exception as err:
###                self.glogger.error("Failed to delete UserId=%s from AAD. err=%s", user_id, err)
###                return False
###            return True
###
###        # ----------------------------------------------------
###        # Delete User from AD
###        # ---------------------------------------------------
###        def delete_user_by_email(self, email: str):
###            user_id = self.get_user_id_by_email(email)
###            if not user_id:
###                return False
###            self.delete_user_by_id(user_id)
###            return True
###
###        # ---------------------------------------------------
###        # Get User's info
###        ## {
###        ## 'additional_properties':
###        ## 	{
###        ## 		'showInAddressList': None,
###        ## 		'userIdentities': [],
###        ## 		'ageGroup': None,
###        ## 		'refreshTokensValidFromDateTime': '2021-06-15T08:48:27Z',
###        ## 		'postalCode': '75550xxx',
###        ## 		'onPremisesSecurityIdentifier': None,
###        ## 		'passwordProfile': None,
###        ## 		'provisionedPlans': [],
###        ## 		'createdDateTime': '2021-04-03T06:23:18Z',
###        ## 		'physicalDeliveryOfficeName': None,
###        ## 		'sipProxyAddress': None,
###        ## 		'state': 'Israel Rabati',
###        ## 		'odata.type': 'Microsoft.DirectoryServices.User',
###        ## 		'provisioningErrors': [],
###        ## 		'telephoneNumber': None,
###        ## 		'proxyAddresses': [],
###        ## 		'country': None,
###        ## 		'preferredLanguage': None,
###        ## 		'legalAgeGroupClassification': None,
###        ## 		'thumbnailPhoto@odata.mediaEditLink':
###        ## 		'directoryObjects/6d0a6552-d57f-4b65-9085-6c2889a948bb/Microsoft.DirectoryServices.User/thumbnailPhoto',
###        ## 		'facsimileTelephoneNumber': None,
###        ## 		'onPremisesDistinguishedName': None,
###        ## 		'isCompromised': None, 'lastDirSyncTime': None,
###        ## 		'department': None, 'otherMails': [],
###        ## 		'consentProvidedForMinor': None,
###        ## 		'streetAddress': 'Goldberg 5tttt',
###        ## 		'passwordPolicies': 'DisablePasswordExpiration',
###        ## 		'userState': None,
###        ## 		'companyName': None,
###        ## 		'dirSyncEnabled': None,
###        ## 		'assignedLicenses': [],
###        ## 		'jobTitle': '035659593556',
###        ## 		'employeeId': None, 'mobile': None,
###        ## 		'extension_12b59af7a1fe40bf9dfc75a94f9a7111_Address': 'kkkk',
###        ## 		'creationType': 'LocalAccount',
###        ## 		'city': 'Rishon',
###        ## 		'extension_12b59af7a1fe40bf9dfc75a94f9a7111_Phone': '+972-53-5659593-111',
###        ## 		'userStateChangedOn': None, 'assignedPlans': []
###        ##     },
###        ## 	'object_id': '6d0a6552-d57f-4b65-9085-6c2889a948bb',
###        ## 	'deletion_timestamp': None,
###        ## 	'object_type': 'User',
###        ## 	'immutable_id': None,
###        ## 	'usage_location': None,
###        ## 	'given_name': 'Danny',
###        ## 	'surname': 'Zadok',
###        ## 	'user_type': 'Member',
###        ## 	'account_enabled': True,
###        ## 	'display_name': 'unknown',
###        ## 	'user_principal_name': '6d0a6552-d57f-4b65-9085-6c2889a948bb@2ndwalletb2c.onmicrosoft.com',
###        ## 	'mail_nickname': '6d0a6552-d57f-4b65-9085-6c2889a948bb',
###        ## 	'mail': None,
###        ## 	'sign_in_names': [<azure.graphrbac.models.sign_in_name_py3.SignInName object at 0x000002414B330CC8>]
###        ## }
###        # ---------------------------------------------------
###        def _get_user_info(self, graphrbac_user) -> dict:
###            # self.glogger.debug("AD-user=%s", graphrbac_user)
###            userdata = {}
###            userdata["userid"] = graphrbac_user.object_id
###            userdata["name"] = graphrbac_user.given_name + " " + graphrbac_user.surname
###            userdata["email"] = self._get_user_email_by_id(graphrbac_user)
###            userdata["mobile"] = graphrbac_user.additional_properties["mobile"]
###            userdata["phone"] = graphrbac_user.additional_properties["jobTitle"]  # Note that we use Job Title to place the phone in
###            userdata["full_address"] = graphrbac_user.additional_properties[
###                "streetAddress"]  # Note that we use Street address to place thefull-address in
###            return userdata
###
###        # ---------------------------------------------------
###        # Get email form the returned dictionary
###        # ---------------------------------------------------
###        def _get_user_email_by_id(self, graphrbac_user: dict) -> str:
###            # if 'mail' in graphrbac_user.keys():
###            if graphrbac_user.mail:
###                email = graphrbac_user.mail
###                email = email.lower()
###                return email
###            if 'otherMails' in graphrbac_user.additional_properties.keys():
###                email_list = graphrbac_user.additional_properties["otherMails"]
###                if len(email_list) > 0:
###                    email = graphrbac_user.additional_properties["otherMails"][0]
###                    email = email.lower()
###                    return email
###            if len(graphrbac_user.sign_in_names) > 0:
###                # print(graphrbac_user.sign_in_names)
###                # print(graphrbac_user.sign_in_names[0].value)
###                email = graphrbac_user.sign_in_names[0].value
###                email = email.lower()
###                return email
###            return None



