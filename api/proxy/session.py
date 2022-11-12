#import json
import uuid
from flask import session
from flask import request

from common.util.logging_helper import get_logger
from common.util.config_wrapper import config_log_session

# -----------------------------------
# Create an instance of the logger
# -----------------------------------
glogger = get_logger("session")

# ---------------------------------------------
# Set the user-flow  (for active drictory)
# ---------------------------------------------
def session_set_user_flow(user_flow : str):
    session["savvly_user_flow"] = user_flow
#    if user_flow == "B2C_1_Savvly_signup_signin" or \
#       user_flow == "B2C_1_Savvly_ria_signup" or \
#       user_flow == "B2C_1_Savvly_user_signup" or \
#       user_flow == "B2C_1_Savvly_signin":
#        glogger.debug("Storing the flow=%s in the session", user_flow)
#    else:
#        glogger.error("Invalid flow=%s passed to store in the session", user_flow)
#    session["savvly_user_flow"] = user_flow

# --------------------------------------------
# Get the user-flow  (for active drictory)
# -----------------------------------------
def session_get_user_flow():
    try:
        user_flow = session["savvly_user_flow"]
    except Exception as err:
        glogger.error("No user-flow found in the session. Expected to find one")
        return None
    return user_flow
#    if user_flow == "B2C_1_Savvly_signup_signin" or \
#       user_flow == "B2C_1_Savvly_ria_signup" or \
#       user_flow == "B2C_1_Savvly_user_signup" or \
#       user_flow == "B2C_1_Savvly_signin":
#        glogger.debug("Retrieving the user-flow from the session: %s", user_flow)
#    else:
#        glogger.error("Invalid flow=%s found in the session", user_flow)
#    return user_flow

# ---------------------------------
# Clear Session  
# ---------------------------------
def session_clear_user():
    session.clear()  # Wipe out user and its token cache from session

# ---------------------------------
# Get Logged User  
# ---------------------------------
def session_is_logged_in():
    if not session_get_user_info():
        return False
    return True

# ---------------------------------
# Get value from the session
# ---------------------------------
def _session_get_value(key: str) -> str:
    if not session_is_logged_in():
        return None
    userinfo = session_get_user_info()
    if not userinfo:
        glogger.error("No userinfo found in the session")
        return None
    #glogger.debug("UserInfo=%s", userinfo)
    if not key in userinfo.keys():
        glogger.info("The key %s is not in the User Info", key)
        #session_print()
        return None
    return userinfo[key]

# ---------------------------------
# Is this a new user 
# ---------------------------------
def session_is_new_user():
    value = _session_get_value('newUser')
    if value is None:
        return False
    if not value:
        return False
    glogger.debug("This is a new user")
    return True

# ---------------------------------
# Get User eMails
# ---------------------------------
def session_get_user_email():
    emails = _session_get_value('emails')
    if not emails:
        return None
    if isinstance(emails, list):
        ret_email =  emails[0]
    elif isinstance(emails, str):
        ret_email = emails
    else:
        glogger.error("The type of emails from session is invalid: %s", type(emails))
        return None
    ret_email = ret_email.lower()
    return ret_email

# ---------------------------------
# Get User First Name
# ---------------------------------
def session_get_user_first_name():
    value = _session_get_value('given_name')
    return value

# ---------------------------------
# Get User Last name
# ---------------------------------
def session_get_user_last_name():
    value = _session_get_value('family_name')
    return value

# ---------------------------------
# Get/Set authentication_mode
# ---------------------------------
#def session_get_auth_mode_as_admin():                return session.get('auth_mode')
#def session_set_auth_mode_as_admin(as_admin:bool):   session["auth_mode"] = as_admin

# ---------------------------------
# Get/Set User Info
# ---------------------------------
def session_get_user_info():            return session.get("user")
def session_set_user_info(userinfo):    session["user"] = userinfo

# ---------------------------------
# Get/Set access token
# ---------------------------------
def session_get_access_token():               return session.get('access_token')
def session_set_access_token(access_token):   session["access_token"] = access_token

# ---------------------------------
# Get/Set access token
# ---------------------------------
def session_get_refresh_token():               return session.get('refresh_token')
def session_set_refresh_token(refresh_token):   session["refresh_token"] = refresh_token

# ---------------------------------
# get Session cache
# ---------------------------------
def session_get_cache():
    return session.get("token_cache")

# ---------------------------------
# Set Session cache
# ---------------------------------
def session_set_cache(cache):
    session["token_cache"] = cache

# ---------------------------------
# Clera Session cache
# ---------------------------------
def session_clear_cache():
    session["token_cache"] = None

# ---------------------------------
# get User Type: Admin/RIA/User
# ---------------------------------
def session_get_user_type():
    #return "savvlyadmin"   # PATCH - TBD - Bypass login
    user_type = session.get("savvly_user_type")
    #print(user_type)
    if user_type == "savvlyclient" or \
       user_type == "savvlyadmin" or \
       user_type == "savvlyvalidatedadvisor" or \
       user_type == "savvlyadvisor":
        glogger.debug("The user type found in the session is: %s", user_type)
        return user_type
    glogger.error("Invalid UserType %s found in the session", user_type)
    return "savvlyclient"

# ---------------------------------
# set User Type: Admin/RIA/User
# ---------------------------------
def session_set_user_type(user_type):
    glogger.debug("Setting the UserType %s in the session", user_type)
    if user_type == "savvlyclient" or \
       user_type == "savvlyadmin" or \
       user_type == "savvlyvalidatedadvisor" or \
       user_type == "savvlyadvisor":
        session["savvly_user_type"] = user_type
        glogger.info("Storing the user type %s in the session", user_type)
        return
    session["savvly_user_type"] = None
    glogger.error("Invalid UserType %s passed to be paced in the session", user_type)
    return

# ---------------------------------
# set specific User Type
# ---------------------------------
def session_set_user_type_as_admin(): session_set_user_type("savvlyadmin")
def session_set_user_type_as_client(): session_set_user_type("savvlyclient")
def session_set_user_type_as_advisor(): session_set_user_type("savvlyadvisor")
def session_set_user_type_as_validated_advisor(): session_set_user_type("savvlyvalidatedadvisor")

# ---------------------------------
# Get User ID
# ---------------------------------
def session_get_user_id():
    value = _session_get_value('oid')
    return value

# ---------------------------------
# Get User Country
# ---------------------------------
def session_get_user_country():
    value = _session_get_value('country')
    return value

# ---------------------------------
# Get User State
# ---------------------------------
def session_get_user_state():
    value = _session_get_value('state')
    return value

# ---------------------------------
# Get User City
# ---------------------------------
def session_get_user_city():
    value = _session_get_value('city')
    return value

# ---------------------------------
# Get User Street
# ---------------------------------
def session_get_user_street():
    value = _session_get_value('streetAddress')
    return value

# ---------------------------------
# Get User Postal Code
# ---------------------------------
def session_get_user_postalcode():
    value = _session_get_value('postalCode')
    return value

# ---------------------------------
# Get User Job Title
# ---------------------------------
def session_get_user_jobtitle():
    value = _session_get_value('jobTitle')
    return value

# ---------------------------------
# Get User Phone Number
# ---------------------------------
def session_get_user_phone_number():
    value = _session_get_value('extension_PhoneNumber')
    return value

# -----------------------------------------------
# Get User CRD Number (Individual)
# -----------------------------------------------
def session_get_user_crd_number():
    value = _session_get_value('extension_crd_number')
    return value

# -----------------------------------------------
# Get Company CRD Number
# -----------------------------------------------
def session_get_company_crd_number():
    value = _session_get_value('extension_company_crd_number')
    return value

# -----------------------------------------------
# Get Company name
# -----------------------------------------------
def session_get_company_name():
    value = _session_get_value('extension_company_name')
    return value

# ---------------------------------
# Dump the session info  
# ---------------------------------
#def session_session_info():
#    if not session_is_logged_in():
#        glogger.error("No user is logged in")
#        return None
#    userinfo = session["user"]
#    return userinfo

# ---------------------------------
# Print Session Info  
# ---------------------------------
def session_print():
    if not config_log_session():
        return
    glogger.info("UserID: %s", session_get_user_id())
    glogger.info("User Type: %s", session_get_user_type())
    glogger.info("IsLoggedin: %s", session_is_logged_in())
    #glogger.debug("IsNewUser: %s", session_is_new_user())
    glogger.info("User Name: %s", session_get_user_first_name())
    glogger.info("Last Name: %s", session_get_user_last_name())
    glogger.info("eMail: %s", session_get_user_email())
    #glogger.info("Country: %s", session_get_user_country())
    glogger.info("State: %s", session_get_user_state())
    #glogger.info("City: %s", session_get_user_city())
    #glogger.info("Street: %s", session_get_user_street())
    #glogger.info("PostalCode: %s", session_get_user_postalcode())
    #glogger.info("AsAdmin: %s", session_get_auth_mode_as_admin())
    glogger.info("Phone: %s", session_get_user_phone_number())
    glogger.info("Individual CRD: %s", session_get_user_crd_number())
    glogger.info("Company CRD: %s", session_get_company_crd_number())
    glogger.info("Company Name: %s", session_get_company_name())
    glogger.info("Session: %s", session)


# ---------------------------------
# Set Random State
# ---------------------------------
def session_set_random_state():
    random_state = str(uuid.uuid4())
    glogger.debug("Setting a random state in the session=%s", random_state)
    session["random_state"] = random_state

# ---------------------------------
# Get  State
# ---------------------------------
def session_get_random_state():
    if not "random_state" in session:
        glogger.error("No random state was stored in the session")
        return None
    random_state = session["random_state"]
    glogger.debug("Getting the random state from the session=%s", random_state)
    return random_state

# ---------------------------------
# Check state  
# ---------------------------------
def session_check_state():
    #print(request.args)
    req_state = request.args.get('state')
    ses_state = session_get_random_state()
    glogger.debug("ReqState=%s SessState=%s", req_state, ses_state)
    if req_state != ses_state:
        glogger.error("The state is not as expected. ReqState=%s SessState=%s", req_state, ses_state)
        return False   # Login Canceled 
    return True




