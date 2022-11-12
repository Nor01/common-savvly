from common.controllers.dbhandles import *
from commontest import *  # Common to all tests in nthis repository
from common.controllers.contract import CheckForNewSignedContracts, Contract
import datetime
from common.controllers.contract import send_promotion_to_client
from common.controllers.contract import DocuSignContractHelper

# g_advisor_id = '37460132-4597-4cd3-8424-237ef753a939'  # yuval_advisor_test
# g_advisor_id = '6a8681ed-e89f-4b9a-b416-b910f3e39d14'  # wil
# g_advisor_id = 'c41ba7be-b4f5-474f-8a32-8d84120ba5e3'  # danny
# g_advisor_id = '2422c75b-f2dc-48f6-b785-5df01714baba'  # home.zadok
# g_advisor_id = 'c41ba7be-b4f5-474f-8a32-8d84120ba5e3'  # dandan
g_advisor_id = '38b62ca1-3c77-4a80-8970-c650ec9c64ee'  # yuval+advisor@savvly.com

# delete threshold in days
g_days_thresh = 7

external_data = {
    'firstname': 'John',
    'lastname': 'Doe (from test script)',
    'address': 'NYC',
    'sex': 'F',
    'birthdate': '1965-01-31',
    'ssn': '123-45-7899',
    'is_married': 'Y',
    'is_US_citizen': 'N',
    'funding': 100000,
    'payout_ages': [111, 65, 70, 100],
    'ETF': 'VOO Vanguard',
    'purchaser_type': 'Accredited Investor',
    # 'investment_start_date': '2023-02-01',
    # optional
    'spouse_firstname': 'Mary',
    'spouse_lastname': 'Jane',
    'spouse_sex': 'F',
    'spouse_birthdate': '1980-12-22',
    'spouse_ssn': '121-45-7777',
    'spouse_email': 'yuval+testscript_spouse@savvly.com',
    'spouse_address': 'Boston MA',
    # must in case of non US citizen
    'passport_data': 'passport data',
    'passport_expiration': '2020-01-02',
    'passport_country': 'Germany',
    'alien_id_or_visa': '123123123',
    'alien_id_or_visa_expiration': '2030-12-31',

}

g_client_info = ClientInfoScheme(**external_data).dict()
g_ts = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M')
g_email = f'yuval+test_script_client_{g_ts}@savvly.com'


def test_create_draft_contract():
    # add to potential client database
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()

    if not clients_table.add_new_client(advisor_id=g_advisor_id, email=g_email, client_info=g_client_info):
        print("Error adding potential client")


def test_send_draft_contract_low_level():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()
    idx, client_info = clients_table.get_client_by_email(advisor_id=g_advisor_id, email=g_email)

    if idx == 0:
        print(f"Did not find {g_email} in contracts")
        return False
    c = Contract(client_email=g_email, client_info=client_info)
    c.send_contract()

    pass


def test_send_draft_contract():
    contract_id = send_promotion_to_client(advisor_id=g_advisor_id, email=g_email)

    print(f"contract_id={contract_id}")


def test_housekeeping():
    infos = CheckForNewSignedContracts()
    print(f"got {len(infos)} newly just signed contracts")
    for info in infos:
        print(f"contract for {info['email']} contract_id={info['contract_id']}")


def get_contract_list_by_status(status: str):
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()

    infos = clients_table.get_all_clients_by_status(advisor_id=g_advisor_id, status=status)
    print(f"List for {status}:")
    for info in infos:
        email = info['email']
        try:
            advisor_id = info['clientinfo']['advisor_id']
        except:
            advisor_id = "None"
        contract_id = info['contractid']
        print(f"{status}|\t{contract_id}|\t{email}\t{advisor_id}")


def get_contract_list():
    get_contract_list_by_status("Draft")
    get_contract_list_by_status("Sent")
    get_contract_list_by_status("Signed")

    # get_contract_list_by_status("Signedasdasd")


def test_get_docusign_info():
    cid = 'c6a15d15-78ab-4178-bb09-c5de3d21b32f'
    cid = '06c3841f-8581-4c40-b7eb-e5fe580095f3'
    c = DocuSignContractHelper(cid)
    info = c.contract_info()
    print(info)
    pass


def test_delete_old_draft_contracts():
    dbh = Dbhandles.get_instance()
    clients_table = dbh.get_potential_clients_tables()

    clients_table.delete_old_records(status='Draft', days_thresh=g_days_thresh)

    clients_table.delete_old_records(status='Sent', days_thresh=g_days_thresh)

    clients_table.delete_old_records(status='Signed', days_thresh=g_days_thresh)

    # clients_table.delete_old_records(status='Signed', days_thresh=8, do_delete=True)


def test_get_signed_contract():
    dbh = Dbhandles.get_instance()
    user_table = dbh.get_usertables()

    users = user_table.get_my_children(parentid=g_advisor_id)
    print(f"found {len(users)} for advisor {g_advisor_id}")

    for user in users:
        idx = user['idx']
        pii = user_table.get_user_pii(idx)['userinfo']
        ##
        print(pii)
        contract = json.loads(user['userinfo'])
        print(json.dumps(contract, indent=4))



gtest_functions = [
    ["Exit", test_exit],
    ["Create draft contract", test_create_draft_contract],
    ["Send draft contract", test_send_draft_contract],
    ["Run House keeping", test_housekeeping],
    ["Get contract list", get_contract_list],
    ["get contract info", test_get_docusign_info],
    ['delete 7 days old draft contracts', test_delete_old_draft_contracts],
    ['Get signed contract from user list', test_get_signed_contract],

    # ["Exit", test_exit],

]


def show_advisor_info(advisor_id):
    dbh = Dbhandles.get_instance()
    ria_table = dbh.get_RIAtables()

    rec = ria_table.get_advisor_info(advisor_id)['advisorinfo']
    rec = json.loads(rec)

    print(json.dumps(rec, indent=4))


if __name__ == "__main__":
    print("Testing contract flow:")
    print(f"Advisor_id={g_advisor_id} client_email={g_email}")
    show_advisor_info(g_advisor_id)
    test_run_menu(gtest_functions)
