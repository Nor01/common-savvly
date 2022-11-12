import json

from pydantic import ValidationError

from common.models.client_info_schema import ClientInfoScheme, split_pii_info, pii_list

tests = []
# married
external_data = {
    'firstname': 'John',
    'lastname': 'Doe',
    'middlename': 'the 2nd',
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
    'investment_start_date': '2023-02-01',
    # optional
    'spouse_firstname': 'Mary',
    'spouse_lastname': 'Jane',
    'spouse_middlename': 'Mama',
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
    'advisor_fee': 11.2  # converted to int

}
tests += [external_data]
# not married
external_data = {
    'firstname': 'John',
    'lastname': 'Doe',
    'address': 'NYC',
    'sex': 'F',
    'birthdate': '1965-01-31',
    'ssn': '123-45-7899',
    'is_married': 'N',
    'is_US_citizen': 'N',
    'funding': 11,
    'payout_ages': [111, 65, 70, 100],
    'ETF': 'VOO Vanguard',
    'purchaser_type': 'Accredited Investor',
    'investment_start_date': '2023-02-01',
    # optional
    # 'spouse_firstname': 'Mary',
    'spouse_lastname': 'Jane',
    'spouse_sex': 'F',
    'spouse_birthdate': '1980-12-22',
    'spouse_ssn': '121-45-7777',
    'spouse_email': 'mail+123@gmail.com',
    'spouse_address': 'Boston MA',
    # must in case of non US citizen
    'passport_data': 'passport data',
    'passport_expiration': '2020-01-02',
    'passport_country': 'Germany',
    'alien_id_or_visa': '123123123',
    'alien_id_or_visa_expiration': '2030-12-31',
    'email': 'yuval+1@savvly.com'
}
tests += [external_data]

# wills test minimal
external_data = {
    "firstname": "Wil",
    "lastname": "Paiz", "email": "xorayac911@leupus.com", "address": "st 100 foo ", "zip_code": "21211",
    "birthdate": "1993-07-11", "sex": "M", "is_US_citizen": "Y", 'is_married': 'N', "ssn": "123-12-3123",
    "investment_start_date": "2022-07-20", "payout_ages": ["65"], "ETF": "VOO Vanguard", "funding": "123456",
    "purchaser_type": "Qualified Purchaser"}

tests += [external_data]

for external_data in tests:
    try:
        user = ClientInfoScheme(**external_data)
        print(json.dumps(json.loads(user.json()), indent=4))
        pii, non_pii = split_pii_info(user.dict(), pii_list)
        print("pii:", pii)
        print("non_pii:", non_pii)

    except ValidationError as e:
        print(json.dumps(json.loads(e.json()), indent=4))
