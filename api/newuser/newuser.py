from common.util.logging_helper import get_logger
from common.util.config_wrapper import get_config_string_param
# from common.activedir.activedir_wrapper import *
from common.msgraph.msgraphapp import *
from common.email.email_helper import *
from common.controllers.dbhandles import *
from proxy.usertype import UserType
from proxy.session import *
from common.controllers.contract_storage import *


# ---------------------------------------------------
# A class to handle a new registerd user
# ---------------------------------------------------
class NewUser:

    # ---------------------------------------------------
    # Constructor
    # ---------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("newuser")
        # self.activedir = AzureADWrapper.get_instance()
        # self.msgraph = MsGraphApp.get_instance()
        self.msgraph = MsGraphApp()
        # self.dbhandles = Dbhandles.get_instance()  # Get the instance of the dbhandles
        # self.admins_id = UserType.get_instance().get_admins()

    # ---------------------------------------------------
    # Process a new registerd user
    # ---------------------------------------------------
    def process(self, idx: str):
        # is_new = session_is_new_user()
        # if not is_new:
        #    self.glogger.info("This iser (%s) is not new", idx)
        #    return True
        self.glogger.debug("A new user detected: %s", idx)
        try:
            user_info = self.msgraph.get_user_by_id(idx)
            if user_info is None:
                self.glogger.error("Failed to get the user info from MSGraph: %s", idx)
                return False
            ad_userid = user_info["id"]
            ad_mail = user_info["mail"]
            ad_name = user_info["givenName"] + " " + user_info["surname"]
            if ad_userid is None or ad_mail is None or ad_name is None:
                self.glogger.error(
                    "The retreived info from MSgraph does not contain the required information. idx=%s info=%s", idx,
                    user_info)

            if not idx == ad_userid:
                self.glogger.error("The passed ID of the logged user (%s) is different from the one found in AD: %s",
                                   idx, ad_userid)
                return False
            if not session_get_user_email() == ad_mail:
                self.glogger.error("The email of the logged user (%s) is different from the one found in AD: %s",
                                   session_get_user_email(), ad_mail)
                # return False
        except Exception as err:
            self.glogger.error("Failed to find the user in MSGRAPH by its ID. err=%s", err)
            return False

        try:
            self.glogger.debug("Sending notification to admins, on user=%s", idx)
            return self._notify_admins_on_user_registration(idx, ad_name, ad_mail)
        except Exception as err:
            self.glogger.error("Failed to notify the admins about the new user. err=%s", err)
            return False
        return True

    # ---------------------------------------------------
    # Notify Admin on user registration
    # ---------------------------------------------------
    def _notify_admins_on_user_registration(self, idx: str, user_name, user_email):
        # if len(self.admins_id) < 1:
        #    self.glogger.error("There is no admin configured in the system")
        #    return False
        # self.glogger.debug("There are %d admins to send them email", len(self.admins_id))
        # admin_email_list = []
        # for admin_id in self.admins_id:
        #    try:
        #        admin_email = self.msgraph.get_email_by_id(admin_id)
        #        if admin_email is None:
        #            self.glogger.error("Failed to find the email of the admin: %s", admin_id)
        #            continue
        #        admin_email_list.append(admin_email)
        #    except Exception as err:
        #        self.glogger.error("Failed to send email to admin:%s. err=%s", admin_email, err)
        #        return False
        # self.glogger.info("Sending email to %s (id=%s) about %s %s", admin_email_list, admin_id, user_name, user_email)
        self.glogger.info("Sending email to admins about %s %s", user_name, user_email)
        SendEmail().send_email_to_admin_on_user_signup(user_name,
                                                       user_email,
                                                       idx + " (" + session_get_user_type() + ")")
        return True

    # -------------------------------------------------------------------------------------------------------------
    # Add a new user who has signed the contract
    # The passed dictionary looks like the following:
    # {'firstname':'Wil%2B1','lastname':'Paiz1','email':'x%2B1@leupus.com','address':'st 100 fefaf','zip_code':'21121',
    #  'birthdate':'1998-07-03','sex':'M','is_US_citizen':'Y','is_married':'Y','ssn':'123-12-3123',
    #  'spouse_firstname':'jess','spouse_lastname':'violl','spouse_birthdate':'1999-07-11','spouse_sex':'F',
    #  'spouse_ssn':'123-12-3123','spouse_is_US_citizen':'Y','spouse_address':'st 100 fefaf 222',
    #  'spouse_email':'xorayac911@leupus.com','investment_start_date':'2022-07-11','payout_ages':[70],
    #  'ETF':'VOO Vanguard','funding':'100000','purchaser_type':'Qualified Purchaser'}"
    # -------------------------------------------------------------------------------------------------------------
    def process_new_signed_client(self, client_info: dict):
        try:
            email = client_info["email"]
            firstname = client_info["firstname"]
            lastname = client_info["lastname"]
            advisor_id = client_info["advisor_id"]
            user_id = self.msgraph.get_id_by_email(email)
            if user_id:
                self.glogger.error("New user process failed. The user already exists in the AD: %s, idx=%s", client_info, user_id)
                return False
            usersinfo = self.msgraph.create_new_user(firstname, lastname, email)
            if usersinfo is None:
                self.glogger.error("failed to create a user in AD (%s %s %s)", firstname, lastname, email)
                return False
            user_id = self.msgraph.get_id_by_email(email)
            if user_id is None:
                self.glogger.error("Failed to get user ID from AAD (%s), even though just created", email)
                return False
            result = Dbhandles.get_instance().get_usertables().add_new_user(user_id, client_info, parent_id=advisor_id)
            if not result:
                self.glogger.error("Failed to add the new signed user to the DB: %s", client_info)
                return False
        except Exception as err:
            self.glogger.error("Failed to process the new user who has signed a contract: %s, err=%s", client_info, err)
            return False
        self.glogger.info("A new used signed a contract and added to AAD and to the DB : %s - Sending email", client_info)

        try:
            #-------------------------------------------------------------------------------
            # Upload the contract to the server
            #-------------------------------------------------------------------------------
            contract_url = client_info['contracturl']
            contract_id = client_info['contract_id']
            advisor_name = client_info['advisor_id']
            client_name = client_info["firstname"] + " " + client_info["lastname"]
            ContractStorage().store(contract_url, contract_id, advisor_name, client_name, user_id)
        except Exception as err:
            self.glogger.error("Failed to upload the signed contract to the storage. client=%s err=%s", client_info, err)

        #-------------------------------------------------------------------------------
        # Send an email to the admins to notify
        #-------------------------------------------------------------------------------
        client_info["userid"] = user_id # Add the new user-id to the client dictionary
        SendEmail().send_email_to_admin_on_client_contract_sign(client_info)  # Notify by email
        return True
