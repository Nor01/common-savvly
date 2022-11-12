import json
from commontest import *  # Common to all tests in nthis repository

from common.util.config_wrapper import ReadConfig

import requests

contract_config = ReadConfig.get_instance().get_string_value("contract")

data = {
    "documents": [{
        "name": "Savvly New Subscriber Contract",
        "doc_id": "NEW_SUBSCRIBER_CONTRACT",
        "document_data": {
            "phone": "+1 (555) 555-5555",
            "spouse_firstname": "Suzie",
            "state": "CO",
            "zip_code": "12345-1234",
            "email": "sly.investor@invesco.com",
            "is_US_citizen": "Y",
            "purchaser_type": "Qualified Purchaser",
            "investor_accredited_gt_1mm": "Y",
            "firstname": "Sylvester",
            "ssn": "111-22-3333",
            "birthdate": "1/2/34",
            "payout_ages": [65, 68, 70],
            "citizenship": "US",
            "address": "123 Main St",
            "is_qualified_purchaser": "N",
            "funding": "100000",
            "investor_sufficient_knowledge": "Y",
            "spouse_lastname": "Spouse",
            "lastname": "Investor",
            "investor_accredit_gt_200k": "Y",
            "city": "Denver"
        }
    }],

    "signers": [
        {
            "signer_email": "yuval@savvly.com",
            "signer_name": "Yuval Rav",
            "sign_here_marker": "CLIENT_SIGN_HERE",
            "sign_date_marker": "CLIENT_DATE_SIGNED"
        },
        {
            "signer_email": "yuval@savvly.com",
            "signer_name": "Yuval (Spouse)",
            "sign_here_marker": "CLIENT_SPOUSE_SIGN_HERE",
            "sign_date_marker": "CLIENT_SPOUSE_DATE_SIGNED"
        },
        contract_config['savvly_signer'],
        # {
        #     "signer_email": "yuval@savvly.com",
        #     "signer_name": "Yuval (Savvly)",
        #     "sign_here_marker": "SAVVLY_SIGN_HERE",
        #     "sign_date_marker": "SAVVLY_DATE_SIGNED"
        # }
    ],
    "cc": contract_config['cc'],

}

contract_config = ReadConfig.get_instance().get_string_value("contract")
docusign_service_url = contract_config['docusign_service_url']
template_service_render_url = contract_config['template_service_render_url']
template_service_url = contract_config['template_service_url']

# creating a docusign document
# res = requests.post(url=docusign_service_url, json=data)
#
# print(res.status_code, res.reason, res.content)
#
# get required params
# res = requests.get(url=template_service_url)
# print("status_code=", res.status_code)
# print(json.dumps(res.json(), indent=4))

# render
res = requests.post(url=template_service_render_url, params={"output": "pdf"},
                    json={'document_data': data['documents'][0]['document_data'], }, )
print("status_code=", res.status_code, res.reason)
file = open("test_doc.pdf", "wb")
file.write(res.content)
file.close()
