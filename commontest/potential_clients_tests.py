from common.controllers.dbhandles import *
# from tests import test_print_result
# from tests import test_get_user_selection, test_get_integer_input, test_exit
from commontest import *  # Common to all tests in nthis repository
from common.controllers.contract import CheckForNewSignedContracts


# -------------------------------------------------------------------------
# Create a list of users
# -------------------------------------------------------------------------
def test_create_clients():
    # print("testing RIA database")
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()

    for userinfo in guser_list:
        advisor_id, email, contract_id, client_info = userinfo

        # print(f"adding user idx={idx}")
        if not clients_table.add_new_client(advisor_id=advisor_id, email=email, client_info=client_info):
            break


# -------------------------------------------------------------------------
# get_all_associated_RIAs
# -------------------------------------------------------------------------
def test_get_all_clients():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()
    advisor_id = guser_list[0][0]

    clients = clients_table.get_all_clients_by_status(advisor_id, '*')
    test_print_result(f"clients associated with '{advisor_id}':", clients)


def test_housekeeping_signed():
    CheckForNewSignedContracts()


# -------------------------------------------------------------------------
# test_get_all_sent_contracts
# -------------------------------------------------------------------------
def test_get_all_sent_contracts():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()
    clients = clients_table.get_all_sent_contracts()
    test_print_result(f"all sent contracts':", clients)


# -------------------------------------------------------------------------
# get_all_associated_RIAs with status PotentialClient
# -------------------------------------------------------------------------
def test_get_all_clients_status_Draft():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()
    advisor_id = guser_list[0][0]
    status = 'Draft'
    clients = clients_table.get_all_clients_by_status(advisor_id, status)
    test_print_result(f"{status} clients associated with '{advisor_id}':", clients)


# -------------------------------------------------------------------------
# test_delete_potential_customer_table
# -------------------------------------------------------------------------
def test_delete_potential_customer_table():
    dbh = Dbhandles.get_instance()
    res = dbh.delete_potential_clients_tables()
    test_print_result(f"delete result", res)


# -------------------------------------------------------------------------
# test_delete_client
# -------------------------------------------------------------------------
def test_delete_client():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()
    advisor_id = guser_list[0][0]
    email = guser_list[0][1]

    clients_table.delete_client(advisor_id, email)


# -------------------------------------------------------------------------
# test_delete_potential_customer_table
# -------------------------------------------------------------------------
def test_update_status():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()

    advisor_id = guser_list[0][0]
    email = guser_list[0][1]

    # test set a bad status
    clients_table.set_client_status(advisor_id, email, 'XYZ')
    # test set a status
    clients_table.set_client_status(advisor_id, email, 'Sent')


# -------------------------------------------------------------------------
# test_send_promotion
# -------------------------------------------------------------------------
def test_send_promotion():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()

    advisor_id = guser_list[0][0]
    email = guser_list[0][1]
    contract_id = guser_list[0][2]
    clients_table.send_promotion_to_client(advisor_id, email)


# ----------------------s---------------------------------------------------
# The RIA  potential customer list
# -------------------------------------------------------------------------
guser_list = [
    # 0             1           2               3       4
    # advisor_id      email      contractid, clientinfo
    ["Advisor1", "yuval+pot_test_client@gmail.com", "contract_1",
     {
         'firstname': 'John',
         'lastname': 'Doe',
         'address': "NYC's",
         'sex': 'F',
         'birthdate': '1965-01-31',
         'ssn': '123-45-7899',
         'is_married': 'Y',
         'is_US_citizen': 'N',
         'funding': 11,
         'payout_ages': [111, 65, 70, 100],
         'ETF': 'VOO Vanguard',
         'purchaser_type': 'Accredited Investor',
         'investment_start_date': '2023-02-01',
         # optional
         'spouse_firstname': 'Mary',
         'spouse_lastname': 'Jane',
         'spouse_sex': 'F',
         'spouse_birthdate': '1980-12-22',
         'spouse_ssn': '121-45-7777',
         'spouse_email': 'mail@gmail.com',
         'spouse_address': 'Boston MA',
         # must in case of non US citizen
         'passport_data': 'passport data',
         'passport_expiration': '2020-01-02',
         'passport_country': 'Germany',
         'alien_id_or_visa': '123123123',
         'alien_id_or_visa_expiration': '2030-12-31',

     }],

]
g_associated = 'savvly'

# -------------------------------------------------------------------------
# The lookup table for the supported test functions
# -------------------------------------------------------------------------
gtest_functions = [
    ["Exit", test_exit],
    ["Create potential clients in the database", test_create_clients],
    ["Get all clients", test_get_all_clients],
    ["Get all Draft Clients", test_get_all_clients_status_Draft],
    ["Delete potential clients table", test_delete_potential_customer_table],
    ["Set status", test_update_status],
    ["Set client status to deleted", test_delete_client],
    ["Send promotion to client", test_send_promotion],
    ["Get all sent contracts", test_get_all_sent_contracts],
    ["Run housekeeping signed", test_housekeeping_signed]

]

if __name__ == "__main__":
    test_run_menu(gtest_functions)
