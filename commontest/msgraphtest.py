from common.email.email_helper import *
from common.msgraph.msgraphapp import *
from  commontest import *  # Common to all tests in nthis repository

gidx = "3f8e9190-adf9-4d9d-a6f6-060c4b0b68eb" #Dandan

# -------------------------------------------------------------------------
# Get the info of the logged-in user
# -------------------------------------------------------------------------
def test_msgraph_get_my_info():
    msgraph = MsGraphApp()
    userlist = msgraph.get_user_by_id(gidx)
    print(userlist)
    #msgraph = MsGraphUser.get_instance()
    #userinfo = msgraph.get_my_info()
    #print(userinfo)

# -------------------------------------------------------------------------
# Get list of users from Active Directory
# -------------------------------------------------------------------------
def test_msgraph_get_users():
    msgraph = MsGraphApp()
    userlist = msgraph.get_users_list()
    print(userlist)

# -------------------------------------------------------------------------
# Get User email by id
# -------------------------------------------------------------------------
def test_msgraph_get_email_by_id():
    msgraph = MsGraphApp()
    email = msgraph.get_email_by_id(gidx)
    print(email)

# -------------------------------------------------------------------------
# Get list of users email from Active Directory
# -------------------------------------------------------------------------
def test_msgraph_get_users_email():
    msgraph = MsGraphApp()
    emaillist = msgraph.get_all_users_email()
    print(emaillist)

# -------------------------------------------------------------------------
# Get User ID by email
# -------------------------------------------------------------------------
def test_msgraph_get_id_by_email():
    email = "Dandan.zadok@gmail.com"
    msgraph = MsGraphApp()
    id = msgraph.get_id_by_email(email)
    print(id)

# -------------------------------------------------------------------------
# Create a new user
# -------------------------------------------------------------------------
def test_msgraph_create_new_user():
    msgraph = MsGraphApp()
    base = "Test3"
    #result = msgraph.create_new_user(base, base+"LastName", base+"@savvlyb2c.onmicrosoft.com")
    result = msgraph.create_new_user(base, base+"LastName", base+"@gmail.com")
    print(result)
    if result:
        idx = result["id"]
        result = msgraph.update_user_address(idx, base+"street", base+"city", base+"zip")

# -------------------------------------------------------------------------
# Reset Password
# -------------------------------------------------------------------------
def test_msgraph_reset_password():
    msgraph = MsGraphApp()
    result = msgraph.reset_password(gidx)
    print(result)

# -------------------------------------------------------------------------
# Send eMail - User registration
# -------------------------------------------------------------------------
def test_send_email_on_registration():
    to_addr = "danny@savvly.com"
    subject = "Savvly Test Subject"
    body = "This is a test"
    mailer = SendEmail()
    mailer.send_email_to_admin_on_user_signup("danny zadok", "stam@email.com", "stamid")

# -------------------------------------------------------------------------
# Send eMail - User signed contract
# -------------------------------------------------------------------------
def test_send_email_on_contract_sign():
    client_info = {'firstname': 'YYY', 'lastname': 'YYYYYY', 'email': 'YYY@leupus.com', 'address': 'YYYYYY',
                   'zip_code': '21121', 'birthdate': '1998-07-03', 'sex': 'M', 'is_US_citizen': 'Y', 'is_married': 'Y',
                   'ssn': '123-12-3123',
                   'spouse_firstname': 'YYY', 'spouse_lastname': 'YYY', 'spouse_birthdate': '1999-07-11',
                   'spouse_sex': 'F',
                   'spouse_ssn': '123-12-3123', 'spouse_is_US_citizen': 'Y', 'spouse_address': 'YYYYYYYYY',
                   'spouse_email': 'YYY@leupus.com', 'investment_start_date': '2022-07-11', 'payout_ages': [70],
                   'ETF': 'VOO Vanguard', 'funding': '100000', 'purchaser_type': 'Qualified Purchaser'}
    mailer = SendEmail()
    mailer.send_email_to_admin_on_client_contract_sign(client_info)

#-------------------------------------------------------------------------
# The lookup table for the supported test functions
#-------------------------------------------------------------------------
gtest_functions = [
    ["Exit",                                                                 test_exit],
    ["MSGraph - Get the info of specific userid",                            test_msgraph_get_my_info],
    ["MSGraph - Get All Users",                                              test_msgraph_get_users],
    ["MSGraph - User email by ID",                                           test_msgraph_get_email_by_id],
    ["MSGraph - Get All Users Email",                                        test_msgraph_get_users_email],
    ["MSGraph - Get User ID by email",                                       test_msgraph_get_id_by_email],
    ["MSGraph - Create a new user",                                          test_msgraph_create_new_user],
    ["MSGraph - Reset Password",                                             test_msgraph_reset_password],
    ["Send Email on Registration",                                           test_send_email_on_registration],
    ["Send Email on contract sign",                                          test_send_email_on_contract_sign],
    #["Reserved",                                                             test_stub],
]

#-------------------------------------
# The program starts here
#-------------------------------------
if __name__ == "__main__":
    test_run_menu(gtest_functions)
