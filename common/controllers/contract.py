import requests
# from common.models.client_info_schema import ClientInfoScheme
import json
import base64
from common.controllers.dbhandles import Dbhandles
from common.models.db_potential_clients import *
from common.util.config_wrapper import ReadConfig
from common.util.logging_helper import get_logger


def CheckForNewSignedContracts():
    glogger = get_logger("housekeeping_check_signed")
    # get all non-signed contract list
    glogger.info("CheckForNewSignedContracts")

    dbh = Dbhandles.get_instance()
    db = dbh.get_potential_clients_tables()

    sent_contracts = db.get_all_sent_contracts()

    glogger.info(f"found {len(sent_contracts)} sent contracts")

    # per contract check if it is signed

    client_infos = []
    for contract in sent_contracts:
        contract_id = contract["contractid"]
        DS = DocuSignContractHelper(contract_id)
        info = DS.contract_info()
        client_info = contract['clientinfo']
        glogger.info(f"contract contract_id={client_info['contract_id']} email={client_info['email']}")
        if info:
            # glogger.info(info)
            signers = info['envelope']['signers']
            # take the first signer date (todo: case of spouse)
            # todo: change this to signed by all parties (completed?)
            # signed_date = signers[0]['signed_date_time']
            signed_date = info['envelope']['completed_date_time']
            if signed_date is not None:
                # client_info = contract['clientinfo']
                client_info['signed_date'] = signed_date.split('T')[0]
                glogger.info(f"found contract signed date {signed_date} for {client_info['email']} updating status to Sent")

                db.update_record_after_signed(idx=contract['idx'], advisor_id=contract['advisorid'],
                                              contract_id=contract_id, client_info=client_info)

                client_infos += [client_info]
    return client_infos


class Contract:
    def __init__(self, client_email: str, client_info: dict):
        self.glogger = get_logger("contract")
        self.contract_id = None
        self.contract_config = ReadConfig.get_instance().get_string_value("contract")
        self.docusign_service_url = self.contract_config['docusign_service_url']
        self.docusign_service_retrieve_url = self.contract_config['docusign_service_retrieve_url']
        self.template_service_url = self.contract_config['template_service_render_url']

        self.client_email = client_email
        self.contract_data = client_info
        ## add additional parameters for the contract
        self.contract_data['email'] = client_email
        self.contract_data['investor_accredit_gt_200k'] = 'Y'
        self.contract_data['investor_accredited_gt_1mm'] = 'Y'
        self.contract_data['is_qualified_purchaser'] = 'N'
        self.contract_data['investor_sufficient_knowledge'] = 'Y'

        if client_info['is_US_citizen'] == 'Y':
            self.contract_data['citizenship'] = 'US'
        else:
            self.contract_data['citizenship'] = client_info['passport_country']

        # signers
        self.signers = [
            {
                "signer_email": client_email,
                "signer_name": client_info['firstname'] + ' ' + client_info['lastname'],
                "sign_here_marker": "CLIENT_SIGN_HERE",
                "sign_date_marker": "CLIENT_DATE_SIGNED"
            },
            # self.contract_config['savvly_signer']
        ]
        if client_info['is_married'] == 'Y':
            self.signers += [{
                "signer_email": client_info['spouse_email'],
                "signer_name": client_info['spouse_firstname'] + ' ' + client_info['spouse_lastname'],
                "sign_here_marker": "CLIENT_SPOUSE_SIGN_HERE",
                "sign_date_marker": "CLIENT_SPOUSE_DATE_SIGNED"
            }]

        self.signers += [self.contract_config['savvly_signer']]

    # todo : add these field to clientinfo scheme
    # city, state, zip_code, email? phone?
    def send_contract(self):
        contact_json = {
            "documents": [
                {"name": "Savvly New Subscriber Contract",
                 "doc_id": "NEW_SUBSCRIBER_CONTRACT",
                 "document_data": self.contract_data}
            ],
            "signers": self.signers,
            "cc": self.contract_config['cc']

        }
        self.glogger.info(f"sending Docusign contract to {self.contract_data['email']}")
        res = requests.post(url=self.docusign_service_url, json=contact_json)

        if res.status_code != 200:
            self.glogger.error(f"failed to create contract: {res.reason}")
            return None

        contract_id = json.loads(res.content)['envelope_id']

        return contract_id

    def preview_contract(self):
        contact_json = {"document_data": self.contract_data}

        self.glogger.info(f"creating draft Docusign contract to {self.contract_data['email']}")
        res = requests.post(url=self.template_service_url, params={"output": "pdf"}, json=contact_json)
        # + "/render?output=pdf"
        if res.status_code != 200:
            self.glogger.error(f"failed to create preview contract: {res.reason}")
            return None

        return base64.b64encode(res.content)


# Helper to access Docusign documents and workflow
class DocuSignContractHelper:
    def __init__(self, contract_id: str):
        self.glogger = get_logger("DocuSignHelper")
        self.contract_id = contract_id
        self.contract_config = ReadConfig.get_instance().get_string_value("contract")
        self.docusign_service_info_url = self.contract_config['docusign_service_info_url']
        self.docusign_service_retrieve_url = self.contract_config['docusign_service_retrieve_url']

    # retrieve contract's pdf from docusign, assumes there is a single contract in the envelope
    def retrieve_contract(self):
        url = self.docusign_service_retrieve_url.format(envelope=self.contract_id)
        self.glogger.info(f"preview Docusign contract {self.contract_id}")

        res = requests.get(url)
        if res.status_code != 200:
            self.glogger.error(f"failed to retrive contract {self.contract_id}: {res.reason}")
            return None
        return base64.b64encode(res.content)

    # retrieve contract's info from docusign, assumes there is a single contract in the envelope
    def contract_info(self):
        url = self.docusign_service_info_url.format(envelope=self.contract_id)
        self.glogger.info(f"getting info for Docusign contract {self.contract_id}")

        res = requests.get(url)
        if res.status_code != 200:
            self.glogger.error(f"failed to retrive contract {self.contract_id}: {res.reason}")
            return None
        return json.loads(res.content)


# -----------------------------------
# send contract via docusign service and set status to SENT
# -----------------------------------
def send_promotion_to_client(advisor_id: str, email: str) -> str:
    # get client's info from potential client
    dbh = Dbhandles.get_instance()
    db = dbh.get_potential_clients_tables()
    idx, client_info = db.get_client_by_email(advisor_id, email)

    if idx == 0:
        return False

    # send the contract
    contract = Contract(client_email=email, client_info=client_info)

    contract_id = contract.send_contract()

    client_info['contract_id'] = contract_id
    client_info['email'] = email
    # maybe add here  client_info sent date.???

    # update record with client info and contract id

    db.update_record_after_sent(idx=idx, advisor_id=advisor_id, contract_id=contract_id, client_info=client_info)

    return contract_id
