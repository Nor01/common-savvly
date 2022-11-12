from common.controllers.deaduser import *
from commontest import *  # Common to all tests in nthis repository


external_data = {
    'firstname': 'John',
    'lastname': 'Doe',
    'address': 'NYC',
    'sex': 'F',
    'birthdate': '1965-01-31',
    'ssn': '123-45-7899',
    'is_married': 'Y',
    'is_US_citizen': 'N',
    'funding': 11,
    'payout_ages': [111, 65, 70, 100],
    'ETF': 'VOO Vanguard',
    'purchaser_type': 'Accredited Investor',
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

}

try:
    user = ClientInfoScheme(**external_data)
    print(json.dumps(json.loads(user.json()), indent=4))
    pii, non_pii = split_pii_info(user.dict(), pii_list)
    print("pii:", pii)
    print("non_pii:", non_pii)

    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    idx = 'Usr_test_usertables'
    ret = usertable.add_new_user(idx, user.dict())
    print(ret)

    user = usertable.get_user_pii(idx)
    saved_pii = json.loads(user['userinfo'])
    user_rec = usertable.get_table_row_values(idx, usertable.tab_name_data)
    user_saved_userinfo = json.loads(user_rec['userinfo'])
    print("saved pii:")
    print(json.dumps(saved_pii, indent=4))
    print("saved contract info:")
    print(json.dumps(user_saved_userinfo, indent=4))
    pass
except ValidationError as e:
    print(json.dumps(json.loads(e.json()), indent=4))
