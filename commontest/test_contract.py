from commontest import *
from common.controllers.contract import Contract, send_promotion_to_client

client_info = {
    "phone": "+1 (555) 555-5555",
    "spouse_firstname": "Suzie",
    "state": "CO",
    "zip_code": "12345-1234",
    # "email": "sly.investor@invesco.com",
    "is_married": 'Y',
    "is_US_citizen": "Y",
    "purchaser_type": "Qualified Purchaser",
    "investor_accredited_gt_1mm": "Y",
    "firstname": "Sylvester",
    "ssn": "111-22-3333",
    "birthdate": "43-12-31",
    "payout_ages": [65, 68, 70],
    # "citizenship": "US",
    "address": "123 Main St",
    "is_qualified_purchaser": "N",
    "funding": "100000",
    "investor_sufficient_knowledge": "Y",
    "spouse_lastname": "Spouse",
    "lastname": "Investor",
    "investor_accredit_gt_200k": "Y",
    "city": "Denver",
    "spouse_email": 'yuval+spouse@savvly.com'
}

cid=send_promotion_to_client(advisor_id="Advisor1", email="yuval+testhtml2@savvly.com")
print(cid)

c = Contract(client_email='yuval+clientmail@savvly.com', client_info=client_info)

res = c.preview_contract()
if res is None:
    print("error in call")
else:
    print(f"produced pdf length {len(res)}")

res = c.send_contract()
print(res)
