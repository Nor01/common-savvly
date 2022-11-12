from datetime import datetime
from typing import Literal
import datetime

from pydantic import ValidationError, BaseModel, EmailStr

from common.database.db_tablecollection import *
from common.models.client_info_schema import ClientInfoScheme
from common.util.utility_functions import *

# from common.controllers.contract import Contract

STATUS_CREATED_DRAFT = 'Draft'
STATUS_SENT = 'Sent'
STATUS_SIGNED = 'Signed'
STATUS_REJECTED = 'Rejected'
STATUS_PAID = 'Paid'
STATUS_PAYMENT_CONFIRMED = 'PaymentConfirmed'
status_values = [STATUS_CREATED_DRAFT, STATUS_SENT, STATUS_SIGNED, STATUS_REJECTED, STATUS_PAID,
                 STATUS_PAYMENT_CONFIRMED]


class potential_schema(BaseModel):
    advisorid: str
    email: EmailStr
    contractid: str
    clientinfo: str
    status: Literal[
        STATUS_CREATED_DRAFT, STATUS_SENT, STATUS_SIGNED, STATUS_REJECTED, STATUS_PAID, STATUS_PAYMENT_CONFIRMED]
    lastupdate: str


#
# -----------------------------------------------------------------------------------------------------------------------
# potential clients - contracts management table
# -----------------------------------------------------------------------------------------------------------------------
#
# potential clients table [RIAid, email, contractid, clientinfo, last_update]
#
class DbPotentialClientsTables(DbTableCollection):
    tab_name_data = "potentialclients"  # Potential clients data Table

    col_name_timestamp = "idx"  # This is the primary key - must be "idx" - do not change it
    col_name_advisor_id = "advisorid"  # Advisor ID (provided as OID by Active Directory)
    col_name_email = "email"  # potential client Email address
    col_name_contract_id = "contractid"  # contract ID from DocuSign
    col_name_client_info = "clientinfo"  # client info - dictionary of info for contract
    col_name_status = "status"  # status of contract
    col_name_lastupdate = "lastupdate"

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbPotentialclientTable")
        tables_info = self._build_tables_info()
        self.empty_contract = "None"
        super().__init__(tables_info)

    # ----------------------------------------------------------------------
    # Create potential client table
    # ----------------------------------------------------------------------
    def _build_tables_info(self):
        tables_info = {self.tab_name_data: [
            (self.col_name_timestamp, 'text PRIMARY KEY'),
            (self.col_name_advisor_id, "text"),
            (self.col_name_email, "text"),
            (self.col_name_contract_id, "text"),
            (self.col_name_client_info, "text"),
            (self.col_name_status, "text"),
            (self.col_name_lastupdate, "text"),
        ]}

        return tables_info

    # -----------------------------------
    # Add new potential client
    # -----------------------------------
    def add_new_client(self, advisor_id: str, email: str, client_info: dict):

        # check validity of info dict
        self.glogger.info(f"add_new_client client_info={client_info}")
        try:
            utils_add_creation_time_to_dic(client_info)  # Add creation time to the dictionary
            validated_client_info = ClientInfoScheme(**client_info)
        except ValidationError as e:
            self.glogger.error(f"Data {client_info} validation failed {e.json()}")
            return False
        except Exception as e:
            self.glogger.error(f"Exception occured {e}")
            return False

        self.glogger.info(
            f"Adding advisor_id={advisor_id} email={email} firstname={client_info['firstname']} lastname={client_info['lastname']}")
        status = STATUS_CREATED_DRAFT

        # todo: check if record already exist and update it?
        rows = self.get_rows_specific_two_col_value(self.tab_name_data,
                                                    self.col_name_advisor_id, advisor_id,
                                                    self.col_name_email, email)
        if len(rows) > 0:
            primekey = rows[0]['idx']
            self.glogger.info(f"found {len(rows)} existing records, updating {primekey}")
        else:
            primekey = self._build_primary_key()
            if not self.add_new_idx(primekey):
                return False

        contract_id = self.empty_contract  # at this stage there is no contract yet
        values = {
            self.col_name_advisor_id: advisor_id,
            self.col_name_email: email,
            self.col_name_contract_id: contract_id,
            self.col_name_client_info: validated_client_info.json(),
            self.col_name_status: status,
            self.col_name_lastupdate: utils_get_current_epoch_time()
        }

        try:
            validated_values = potential_schema(**values)
        except ValidationError as e:
            self.glogger.error(f"Data {values} validation failed {e.json()}")
            return False

        self.update_values(primekey, self.tab_name_data, validated_values.dict())

        return True

    # -----------------------------------
    # Add get all sent contracts list
    #
    # -----------------------------------
    def get_all_sent_contracts(self):
        self.glogger.info(f"Getting all sent contracts")

        rows = self.get_rows_specific_col_value(self.tab_name_data,
                                                self.col_name_status, STATUS_SENT)

        # convert clientinfo into dict
        for i in range(len(rows)):
            rows[i][self.col_name_client_info] = json.loads(rows[i][self.col_name_client_info])

        self.glogger.info(f"Found {len(rows)} sent contracts")

        return rows

    # -----------------------------------
    # Add get all potential clients of a RIA by status.
    # status = '*' to get all statuses
    # -----------------------------------
    def get_all_clients_by_status(self, advisor_id: str, status: str = None):
        self.glogger.info(f"Getting potential clients of advisor={advisor_id} with status={status}")

        if not (status in status_values + ['*']):
            self.glogger.error("status '{status}' value is invalid")
            return []

        if status == '*':
            rows = self.get_rows_specific_col_value(self.tab_name_data,
                                                    self.col_name_advisor_id, advisor_id)
        else:
            rows = self.get_rows_specific_two_col_value(self.tab_name_data,
                                                        self.col_name_advisor_id, advisor_id,
                                                        self.col_name_status, status)

        # convert clientinfo into dict
        for i in range(len(rows)):
            rows[i][self.col_name_client_info] = json.loads(rows[i][self.col_name_client_info])

        return rows

    # -----------------------------------
    # set new potential client status
    # if contract_id is not None, update it
    # -----------------------------------
    def set_client_status(self, advisor_id: str, email: str, status: str, contract_id: str = None):
        self.glogger.info(f"Setting RIA={advisor_id} email={email} to status={status}")
        if not (status in status_values):
            self.glogger.error(f"{status} is an invalid value for status")
            return False

        # find the record

        record = self.get_rows_specific_two_col_value(self.tab_name_data,
                                                      self.col_name_advisor_id, advisor_id,
                                                      self.col_name_email, email)

        if not record:
            self.glogger.info(f"no record found")
            return False

        if len(record) > 1:
            self.glogger.info(
                f"There were {len(record)} records found with email={email} for advisor_id={advisor_id}. Using the first found."
            )

        idx = record[0]['idx']

        if contract_id is None:
            contract_id = record[0]['contractid']

        values = {
            self.col_name_contract_id: contract_id,
            self.col_name_status: status,
            self.col_name_lastupdate: utils_get_current_epoch_time()
        }

        self.update_values(idx, self.tab_name_data, values)

        return True

    # -----------------------------------
    # set new potential client status to declined i.e. delete
    # -----------------------------------
    def delete_client(self, advisor_id: str, email: str):
        return self.set_client_status(advisor_id, email, status=STATUS_REJECTED)

    # -----------------------------------
    # set new potential client status to sent i.e. promotion sent
    # -----------------------------------
    def set_client_status_promotion_sent(self, advisor_id: str, email: str, contract_id: str):
        return self.set_client_status(advisor_id, email,
                                      status=STATUS_SENT,
                                      contract_id=contract_id)

    ## helper function for sending contract
    def get_client_by_email(self, advisor_id: str, email: str) -> (int, str):
        # find the record (client with the according to advisor_id and clients email

        record = self.get_rows_specific_two_col_value(self.tab_name_data,
                                                      self.col_name_advisor_id, advisor_id,
                                                      self.col_name_email, email)
        if not record:
            self.glogger.info(f"no record found for email={email} for advisor={advisor_id}")
            return 0, self.empty_contract

        if len(record) > 1:
            self.glogger.info(
                f"There were {len(record)} records found with email={email} for advisor_id={advisor_id}. Using the first found."
            )

        idx = record[0]['idx']
        client_info_json = record[0]['clientinfo']
        client_info = json.loads(client_info_json)

        return idx, client_info

    def update_record_after_signed(self, idx: str, advisor_id: str, contract_id: str, client_info: dict):
        # update the advisor id at the time of signing
        client_info['advisor_id'] = advisor_id
        values = {
            self.col_name_contract_id: contract_id,
            self.col_name_status: STATUS_SIGNED,
            self.col_name_client_info: json.dumps(client_info),
            self.col_name_lastupdate: utils_get_current_epoch_time()
        }
        return self.update_values(idx, self.tab_name_data, values)

    def update_record_after_sent(self, idx: str, advisor_id: str, contract_id: str, client_info: dict):
        # update the advisor id at the time of signing
        client_info['advisor_id'] = advisor_id
        values = {
            self.col_name_contract_id: contract_id,
            self.col_name_status: STATUS_SENT,
            self.col_name_client_info: json.dumps(client_info),
            self.col_name_lastupdate: utils_get_current_epoch_time()
        }

        return self.update_values(idx, self.tab_name_data, values)

    def delete_old_records(self, status, days_thresh: int, do_delete=False)->list:
        self.glogger.info(f"Deleting potential clients records with status={status} older than {days_thresh} days")
        allowed_statuses = [STATUS_SENT, STATUS_CREATED_DRAFT, STATUS_SIGNED]
        if status not in allowed_statuses:
            self.glogger.error(f"can delete only {allowed_statuses} contracts")
            return []
        if days_thresh <= 0:
            self.glogger.error(f"days_thresh should not be negative")
            return []

        rows = self.get_rows_specific_col_value(table_nameinx=self.tab_name_data, col_name=self.col_name_status,
                                                value=status)
        deleted_rows = []
        for row in rows:

            try:
                idx = row['idx']
                lastupdate = row['lastupdate']
                lastupdate = int(lastupdate)
                lastupdate = time.gmtime(lastupdate)
                email = row['email']
            except Exception as e:
                print(f"could not record index={idx} exeption:{e}")
                # self.delete_record(idx)
                continue
            now = time.localtime()
            days_passed = datetime.timedelta(seconds=time.mktime(now) - time.mktime(lastupdate)).days
            # print(f"days passed {days_passed}")
            if days_passed >= days_thresh:
                self.glogger.info(
                    f"[actual delete={do_delete}] found a record with status={status} from {days_passed} days ago (email={email}), idx={idx}")
                deleted_rows += [row]
                if do_delete:
                    self.delete_record(idx)

        return deleted_rows

    @staticmethod
    def _build_primary_key():
        today = datetime.datetime.now()
        primekey = today.strftime("%Y%m%d%H%M%S%f")[:-3]
        return primekey
