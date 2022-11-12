import time
import ast
import json
from pydantic import ValidationError
from common.models.client_info_schema import ClientInfoScheme, split_pii_info, pii_list
from common.util.datetime_parser import datetime_parse, datetime_calc_age
from common.database.db_tablecollection import *
from common.kv.kv_wrapper import AzureKeyVaultWrapper
from common.util.string_helper import hash256
from common.models.deathprobability import dp_get_probability
from common.util.utility_functions import *
from pydantic import BaseModel, ValidationError, conlist, constr
from typing import Optional, Union
from datetime import date


## todo:
# PII -
#
# contracts
#   consider pii information when adding new contract
#   (should it be removed, there is a conflict here, as pii information can change over time, even the name
#   and it is part of the contract)
#   update_contract_status(idx, contract_status)
# lastupdate of record - verify
# change when parentid changes or a status change


### definitions of PII dictionary
class PIIScheme(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    middlename: Optional[str]
    ssn: Optional[constr(regex=r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$')]
    birthdate: Optional[date]
    creation: Optional[int]
    lastupdate: Optional[int]


# -----------------------------------------------------------------------------------------------------------------------
# User Data
# -----------------------------------------------------------------------------------------------------------------------
class DbUserTables(DbTableCollection):
    # tab_name_pii = "userpii"                       # User Private Info (stored in KV)
    tab_name_data = "userdata"  # User data Table

    col_name_userid = "idx"  # User ID (provided as OID by Active Directory)
    # col_name_social = "social"                     # User Social Number - must be at least 4 digits (stored in KV)
    # col_name_dateofbirth = "dateofbirth"           # Date of birth Day/Month/Year (stored in KV)
    # col_name_address = "address"                   # User Address  (stored in KV)
    # col_name_mother_maiden = "mothername"          # User's mother maiden name
    #
    # col_name_sex = "sex"                           # User Sex (Female (F) or Male (M)
    col_name_user_info = "userinfo"  # User info as gathered from the potential client contract (PII are stored in the vault)
    col_name_age = "age"  # User age (calculated from date of Birth)
    col_name_parentid = "parentid"  # User Parent ID (the parent is also a user)
    col_name_accountid = "accountid"  # User Account ID - created upon registration
    col_name_statusflag = "statusflag"  # Status flag
    col_name_fair_market_value = "fmv"  # value of the market (user's assets)
    col_name_fund = "fund"  # The base fund of the user - Should be updated upon deposit/withdraw
    col_name_dayprofit = "dayprofit"
    col_name_totprofit = "totprofit"
    col_name_numshares_from_inheritence = "numshares_inheritence"
    col_name_transferamount = "transferamount"
    col_name_transferid = "transferid"  # The ID of the transaction done by the user

    col_name_numshares = "numshares"
    col_name_shareprice = "shareprice"

    status_flag_active = "Active"  # Active/Idle
    status_flag_pending = "Pending"  # just signed up. no KYC (Know your Customer)
    status_flag_transfer = "Transfer"  # incoming $ pending
    status_flag_transfer_complete = "Transfer-Complete"  # transfer compelete (in our bank account)
    status_flag_purchase_pending = "Purchase-Pending"  # Pending to purchase  shares
    status_flag_withdrawal = "Withdrawal"  # $ leaving
    status_flag_withdrawal_pending = "Withdrawal-Pending"  # $ money in our bank account from a sell
    status_flag_deceased = "Deceased"  # dead
    status_flag_closed = "Closed"  # no activity allowed
    status_flag_transfer_cancel = "Transfer-Cancel"  # Transfer_cancel (timeout)

    no_parent = 'null'

    ## new userstable version
    ##
    ##
    col_name_lastupdate = "lastupdate"  # Last update (changes when parent id change or status change)
    col_name_PII = "pii"  # essential PII's of the user
    col_name_contracts = "contracts"  # list of contracts (JSONs)

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbUserTables")
        tables_info = self._build_tables_info()
        super().__init__(tables_info)

    # ----------------------------------------------------------------------
    # Create all user data tables
    # ----------------------------------------------------------------------
    def _build_tables_info(self):
        tables_info = {}

        tables_info[self.tab_name_data] = [
            (self.col_name_userid, "text PRIMARY KEY"),
            # (self.col_name_sex, "text"),
            (self.col_name_user_info, "text"),
            (self.col_name_age, "text"),
            (self.col_name_parentid, "text"),
            (self.col_name_accountid, "text"),
            (self.col_name_statusflag, "text"),
            (self.col_name_fair_market_value, "text"),
            (self.col_name_fund, "text"),
            (self.col_name_dayprofit, "text"),
            (self.col_name_totprofit, "text"),
            (self.col_name_numshares, "text"),
            (self.col_name_numshares_from_inheritence, "text"),
            (self.col_name_transferamount, "text"),
            (self.col_name_transferid, "text"),
            (self.col_name_lastupdate, "text"),
            ## new records
            (self.col_name_PII, "text"),
            (self.col_name_contracts, "text"),

        ]
        return tables_info

    # -----------------------------------
    # Add new user
    # -----------------------------------
    def add_new_user(self, idx: str, client_info: dict, parent_id=None):

        # check validity of info dict
        try:
            validated_client_info = ClientInfoScheme(**client_info)
        except ValidationError as e:
            self.glogger.error(f"Data {client_info} validation failed {e.json()}")
            return False

        social = validated_client_info.ssn
        date_of_birth = validated_client_info.birthdate
        sex = validated_client_info.sex
        address = validated_client_info.address

        if len(social) < 4:
            self.glogger.error("The SS (%s) value is invalid. It should bt at least 4 characters", social)
            return False
        social_4chars = social[-4:]

        dob = date_of_birth
        if dob is None:
            return False
        age = datetime_calc_age(dob)
        if age < 0:
            self.glogger.error("The date of birth is invalid (%s->%s). The age must be positive (%d)", date_of_birth,
                               dob, age)
            return False
        if age > 120:
            self.glogger.error("The date of birth is invalid (%s->%s). The age exceeds the allowed range (%d)",
                               date_of_birth, dob, age)
            return False
        sex = sex[0]  # Get the first character
        sex = sex.upper()
        if sex != 'F' and sex != 'M':
            self.glogger.error("The user sex is invalid: %s. It should be either 'F' or 'M'", sex)
            return False
        self.glogger.info("Adding IDX=%s social=%s dob=%s (age=%d) address=%s sex=%s", idx, social, dob, age, address,
                          sex)

        if not self.add_new_idx(idx):
            return False

        # accountid = str(int(time.time()))
        accountid = hash256(idx + social_4chars, 8)

        pii, non_pii = split_pii_info(validated_client_info.dict(), pii_list)
        self.glogger.info("pii=%s", pii)
        self.glogger.info("non_pii=%s", non_pii)

        values = {}
        values[self.col_name_userid] = idx
        values[self.col_name_user_info] = json.dumps(pii, default=str)  # use default=str for dumping dates
        # values[self.col_name_social] = social
        # values[self.col_name_dateofbirth] = date_of_birth
        # values[self.col_name_address] = address
        # values[self.col_name_mother_maiden] = mother_name
        AzureKeyVaultWrapper.get_instance().add_secret(accountid, str(values))  # Add the user PII to the KV
        # self.update_values(idx, self.tab_name_pii, values)

        utils_add_creation_time_to_dic(non_pii)  # Add creation time to the dictionary

        values = {}
        # values[self.col_name_sex] = sex  # F or M (Female or Male)
        values[self.col_name_user_info] = non_pii  # dict of values
        values[self.col_name_age] = age  # 0 to 120
        if parent_id is None:
            values[self.col_name_parentid] = self.no_parent  # The user has no parent yet
        else:
            values[self.col_name_parentid] = parent_id
        values[self.col_name_accountid] = accountid  # Creation time too
        values[self.col_name_statusflag] = self.status_flag_pending  # Know your customer
        values[self.col_name_fair_market_value] = "0.0"
        values[self.col_name_fund] = "0.0"
        values[self.col_name_dayprofit] = "0.0"
        values[self.col_name_totprofit] = "0.0"
        values[self.col_name_numshares] = "0.0"
        values[self.col_name_numshares_from_inheritence] = "0.0"
        values[self.col_name_transferamount] = "0.0"
        values[self.col_name_transferid] = "None"
        values[self.col_name_lastupdate] = utils_get_current_epoch_time()

        # values = {}
        # values[self.col_name_depositedamount] = "0.0"
        # values[self.col_name_numshares] = "0"
        # values[self.col_name_shareprice] = "0.0"
        # self.update_values(idx, self.tab_name_tran, values)

        # values = {}
        # values[self.col_name_redistributedamount] = "0.0"
        # values[self.col_name_numshares] = "0"
        # values[self.col_name_shareprice] = "0.0"
        # self.update_values(idx, self.tab_name_inherit, values)

        try:
            PII = PIIScheme(**{
                "firstname": validated_client_info.firstname,
                "lastname": validated_client_info.lastname,
                "middlename": validated_client_info.middlename,
                "ssn": validated_client_info.ssn,
                "birthdate": validated_client_info.birthdate,
            }).dict()
            utils_add_creation_time_to_dic(PII)
            values[self.col_name_PII] = json.dumps(PII, default=str)
        except ValidationError as err:
            glogger.error("Validation err:", err)
            return False
        except Exception as err:
            glogger.error("Validation err:", err)
            return False

        self.update_values(idx, self.tab_name_data, values)

        return True

    # -----------------------------------
    # Is allowed to Change Status Flag?
    # -----------------------------------
    def _is_status_flag_change_allowed(self, cur_status: str, new_status: str):

        # State Transition Table
        #
        # The key of the dict is the current state. The value is a list of allowed states
        # from the current state. If the new state is in the list of allowed states for a given
        # key (current state), then it is allowed.
        state_transitions = {
            self.status_flag_pending: [
                self.status_flag_active
            ],

            self.status_flag_active: [
                self.status_flag_transfer,
                self.status_flag_withdrawal,
                self.status_flag_deceased
            ],

            self.status_flag_transfer: [
                self.status_flag_transfer_complete
            ],

            self.status_flag_transfer_complete: [
                self.status_flag_purchase_pending
            ],

            self.status_flag_purchase_pending: [
                self.status_flag_active
            ],

            self.status_flag_withdrawal: [
                self.status_flag_withdrawal_pending
            ],

            self.status_flag_withdrawal_pending: [
                self.status_flag_active
            ],

            self.status_flag_deceased: [
                self.status_flag_closed
            ]
        }

        result = (cur_status in state_transitions) and (new_status in state_transitions[cur_status])

        if result:
            self.glogger.debug("Table: It is OK to change the status flag from %s to %s", cur_status, new_status)
        else:
            self.glogger.error("Table: It is not allowed to change the status flag from %s to %s", cur_status,
                               new_status)
        return result

    # -----------------------------------------------------
    # Update user data in a specific table: userdata
    # -----------------------------------------------------
    def _update_userdata_values(self, idx: str, data_dict: dict):
        if self.col_name_accountid in data_dict:
            self.glogger.error("No allowed to update account-id in the userdata table for idx=%s", idx)
            return False
        data_dict[self.col_name_lastupdate] = utils_get_current_epoch_time()
        return self.update_values(idx, self.tab_name_data, data_dict)

    # -----------------------------------------------------
    # Update user data in a specific table: inherited
    # -----------------------------------------------------
    # def _update_inherited_values(self, idx: str, data_dict: dict):
    #    return self.update_values(idx, self.tab_name_inherit, data_dict)

    # -----------------------------------
    # Delete an existing user
    # -----------------------------------
    def delete_user(self, idx: str):
        accountid = self.get_col_str_value(idx, self.tab_name_data, self.col_name_accountid)
        if accountid is None:
            self.glogger.error("Could not get account ID of the user=%s", idx)
            return None
        if not AzureKeyVaultWrapper.get_instance().delete_secret(accountid):
            self.glogger.error("Failed to delete the user from the KV. user=%s", idx)
        return self.delete_record(idx)

    # ------------------------------------------
    # Get User Private Info (PII)
    # ------------------------------------------
    def get_user_pii(self, idx: str) -> dict:
        accountid = self.get_col_str_value(idx, self.tab_name_data, self.col_name_accountid)
        if accountid is None:
            self.glogger.error("Could not get account ID of the user=%s", idx)
            return None
        pii_str = AzureKeyVaultWrapper.get_instance().get_secret(accountid)
        self.glogger.info("The user private info (PII) of idx=%s is %s", idx, pii_str)
        try:
            pii_dict = ast.literal_eval(pii_str)
            self.glogger.info("The user private info of idx=%s is %s", idx, pii_dict)
            return pii_dict
        except Exception as err:
            self.glogger.error("Could not convert the PII info of account %s to dictionary:%s err=%s", accountid,
                               pii_str, err)
        return None

    # ------------------------------------------
    # Get User PII column
    # ------------------------------------------
    def get_user_PII(self, idx: str) -> Optional[dict]:
        pii = self.get_col_str_value(idx, self.tab_name_data, self.col_name_PII)
        if pii is None:
            self.glogger.error("Could not get PII of the user=%s", idx)
            return None
        else:
            try:
                pii_dict = json.loads(pii)
                ## json dump to stringify the date time
                return json.loads(PIIScheme(**pii_dict).json())
            except ValidationError as err:
                self.glogger.error(f"Could not convert the PII info of user_id{idx}, pii={pii}, error={err}")
                return None
            except Exception as err:
                self.glogger.error(f"Could not convert the PII info of user_id{idx}, pii={pii}, error={err}")
                return None

    # ------------------------------------------
    # Get User cotract
    # returns list of contracts, otherwise
    # if contract=None just return the list,
    # if contract is a UserSchema adds the contract
    # ------------------------------------------
    def user_contracts(self, idx: str, new_contract: Optional[dict] = None) -> Optional[dict]:
        contracts = self.get_col_str_value(idx, self.tab_name_data, self.col_name_contracts)

        # get current contracts
        try:
            if not contracts:
                contracts = []
            else:
                contracts = ast.literal_eval(contracts)
        except Exception as err:
            glogger.error(f"Something went wrong with data {contracts} err={err}")
            return None

        if new_contract is None:
            try:
                for i in range(len(contracts)):
                    contracts[i] = json.loads(contracts[i])
            except Exception as err:
                glogger.error(f"issue with data loading data={contracts[i]}, err={err}")
            return contracts

        try:
            new_validated_contract = ClientInfoScheme(**new_contract).json()
        except ValidationError as err:
            glogger.error(f"Validation error {err}")
            return contracts
        contracts += [new_validated_contract]
        # update contracts record
        data_dict = {self.col_name_contracts: contracts}
        ret = self._update_userdata_values(idx, data_dict)
        if not ret:
            glogger.error("Unable to update contract")

        try:
            for i in range(len(contracts)):
                contracts[i] = json.loads(contracts[i])
        except Exception as err:
            glogger.error(f"issue with data loading data={contracts[i]}, err={err}")
        return contracts

    # ------------------------------------------
    # Set Parent ID
    # ------------------------------------------
    def set_parentid(self, idx: str, parentid: str):
        cur_parent = self.get_parentid(idx)
        self.glogger.info("Request to change the parent of the user %s from %s to %s", idx, cur_parent, parentid)
        data_dict = {self.col_name_parentid: parentid}
        utils_add_lastupdate_time_to_dic(data_dict)
        return self._update_userdata_values(idx, data_dict)

    # ------------------------------------------
    # Clear Parent ID
    # ------------------------------------------
    def clear_parentid(self, idx: str):
        return self.set_parentid(idx, self.no_parent)

    # ------------------------------------------
    # Get Parent ID
    # ------------------------------------------
    def get_parentid(self, idx: str):
        parentid = self.get_col_str_value(idx, self.tab_name_data, self.col_name_parentid)
        return parentid

    # ------------------------------------------
    # Get Account ID
    # ------------------------------------------
    def get_accountid(self, idx: str):
        accountid = self.get_col_str_value(idx, self.tab_name_data, self.col_name_accountid)
        return accountid

    # ------------------------------------------
    # Get Current inherited shares
    # ------------------------------------------
    def get_inherited_shares(self, idx: str) -> float:
        inherited_shares_str = self.get_col_str_value(idx, self.tab_name_data, self.col_name_numshares_from_inheritence)
        try:
            inherited_shares = float(inherited_shares_str)
        except Exception as err:
            self.glogger.error("The format of inherited_shares is invalid (idx=%s): %s err=%s", idx,
                               inherited_shares_str, err)
            return 0.0
        return inherited_shares

    # ------------------------------------------
    # Get Current Status Flag
    # ------------------------------------------
    def get_status_flag(self, idx: str):
        status_flag = self.get_col_str_value(idx, self.tab_name_data, self.col_name_statusflag)
        return status_flag

    # ------------------------------------------
    # Update Status Flag
    # ------------------------------------------
    def _update_status_flag(self, idx: str, new_status: str):
        cur_status = self.get_status_flag(idx)
        if not self._is_status_flag_change_allowed(cur_status, new_status):
            return False
        self.glogger.info("Changing Status flag of %s from %s to %s", idx, cur_status, new_status)
        data_dict = {self.col_name_statusflag: new_status}
        utils_add_lastupdate_time_to_dic(data_dict)
        return self._update_userdata_values(idx, data_dict)

    # ------------------------------------------
    # Update Status Flag
    # ------------------------------------------
    def set_statusflag_active(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_active)

    def set_statusflag_pending(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_pending)

    def set_statusflag_transfer(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_transfer)

    def set_statusflag_transfer_complete(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_transfer_complete)

    def set_statusflag_purchase_pending(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_purchase_pending)

    def set_statusflag_withdrawal(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_withdrawal)

    def set_statusflag_withdrawal_pending(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_withdrawal_pending)

    def set_statusflag_deceased(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_deceased)

    def set_statusflag_closed(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_closed)

    def set_statusflag_transfer_cancel(self, idx: str):
        return self._update_status_flag(idx, self.status_flag_transfer_cancel)

    # ------------------------------------------
    # Update Inherited Shared
    # ------------------------------------------
    def update_inherited_shares(self, idx: str, inherited_shares: float):
        cur_inherited_shares = self.get_inherited_shares(idx)
        inherited_shares += cur_inherited_shares
        self.glogger.info("Changing inherited shares from %f to %f for user %s", cur_inherited_shares, inherited_shares,
                          idx)
        data_dict = {}
        data_dict[self.col_name_numshares_from_inheritence] = inherited_shares
        return self._update_userdata_values(idx, data_dict)

    # ------------------------------------------
    # Is the status flag active?
    # ------------------------------------------
    def is_active_user(self, idx: str):
        status_flag = self.get_status_flag(idx)
        if status_flag == self.status_flag_active:
            return True
        return False

    # # ------------------------------------------
    # # Do a money transaction
    # # ------------------------------------------
    def _transact_money(self, idx: str, amount: float, transactid: str):
        userdata = self.get_table_row_values(idx, self.tab_name_data)
        if not userdata:  # None or Empty
            self.glogger.error("Failed to get user Data %s", idx)
            return False

        cur_status = userdata[self.col_name_statusflag]
        if cur_status != self.status_flag_active:
            self.glogger.error("The status flag (idx=%s) is not Active (%s). Money Transfer is not allowed", idx,
                               cur_status)
            return False

        cur_amount_str = userdata[self.col_name_transferamount]
        try:
            cur_amount = float(cur_amount_str)
        except Exception as err:
            self.glogger.error("The transfer money in the db (idx=%s) is not a float number:%s err=%s", idx,
                               cur_amount_str, err)
            return False
        if cur_amount != 0:
            self.glogger.error("The transfer money in the db (idx=%s) is not a 0 : %f", idx, cur_amount)
            return False

        cur_fund_str = userdata[self.col_name_fund]
        try:
            cur_fund = float(cur_fund_str)
        except Exception as err:
            self.glogger.error("The fund in the db (idx=%s) is not a float number:%s", idx, cur_fund_str)
            return False

        self.glogger.debug("The user's (%s) fund is going to change from %f to %f", idx, cur_fund, cur_fund + amount)
        cur_fund += amount

        data_dict = {}
        data_dict[self.col_name_transferamount] = str(amount)
        data_dict[self.col_name_fund] = str(cur_fund)
        data_dict[self.col_name_transferid] = transactid
        if amount < 0:
            data_dict[self.col_name_statusflag] = self.status_flag_withdrawal  # Withdrawal
        else:
            data_dict[self.col_name_statusflag] = self.status_flag_transfer  # Deposit
        return self._update_userdata_values(idx, data_dict)

    # ------------------------------------------
    # Deposit money to the account
    # ------------------------------------------
    def deposit_money(self, idx: str, amount: float, transactid: str):
        try:
            if amount <= 0:
                self.glogger.error("The amount of money (%s) to deposit is invalid (id=%s)", str(amount), idx)
                return False
        except Exception as err:
            self.glogger.error("Invalid amount of money to do transaction with (idx=%s):%s err=%s", idx, str(amount),
                               err)
            return False
        return self._transact_money(idx, amount, transactid)

    # ------------------------------------------
    # Withdrawal money from the account
    # ------------------------------------------
    def withdrawal_money(self, idx: str, amount: float):
        try:
            if amount >= 0:
                self.glogger.error("The amount of money (%s) to withdrawal is invalid (id=%s)", str(amount), idx)
                return False
        except Exception as err:
            self.glogger.error("Invalid amount of money to do transaction with (idx=%s):%s err=%s", idx, str(amount),
                               err)
            return False
        return self._transact_money(idx, amount, "None")

    # ------------------------------------------
    # Set Deposit (Transfer) Complete
    # ------------------------------------------
    def set_transfer_complete(self, idx: str):
        userdata = self.get_table_row_values(idx, self.tab_name_data)
        if not userdata:  # None or Empty
            self.glogger.error("Failed to get user Data %s", idx)
            return False
        cur_status = userdata[self.col_name_statusflag]
        if cur_status != self.status_flag_transfer:
            self.glogger.error("The status flag (idx=%s) is not Transfer (%s). No money is in transaction now", idx,
                               cur_status)
            return False
        return self.set_statusflag_transfer_complete(idx)  # Change the state to Transfer Complete

    # ------------------------------------------
    # Set Deposit Complete
    # ------------------------------------------
    def set_purchase_complete(self, idx: str, share_price: float) -> float:
        userdata = self.get_table_row_values(idx, self.tab_name_data)
        if not userdata:  # None or Empty
            self.glogger.error("Failed to get user Data %s", idx)
            return 0.0  # Error
        cur_status = userdata[self.col_name_statusflag]
        if cur_status != self.status_flag_purchase_pending:
            self.glogger.error("The status flag (idx=%s) is not purchase-pending (%s). No money is in transaction now",
                               idx, cur_status)
            return 0.0  # Error
        amount = float(userdata[self.col_name_transferamount])
        if amount <= 0.0:
            self.glogger.error("Invalid amount: idx=%s shareprice=%s amount=%f", idx, share_price, amount)
            return 0.0  # Error
        data_dict = {}
        num_shares_str, new_fmv_str = self._calc_num_shares_after_transaction(share_price,
                                                                              userdata[self.col_name_transferamount],
                                                                              userdata[self.col_name_numshares])

        data_dict[self.col_name_numshares] = num_shares_str
        data_dict[self.col_name_fair_market_value] = new_fmv_str
        data_dict[self.col_name_transferamount] = "0.0"
        data_dict[self.col_name_transferid] = "None"
        data_dict[self.col_name_statusflag] = self.status_flag_active
        result = self._update_userdata_values(idx, data_dict)
        if not result:
            self.glogger.error("Failed to complete the purchase: idx=%s amount=%s shareprice=%s", idx,
                               userdata[self.col_name_transferamount], share_price)
            return 0.0  # Error
        return amount

    # ------------------------------------------
    # Set Withdrawal Complete
    # ------------------------------------------
    def set_withdrawal_complete(self, idx: str, share_price: float):
        userdata = self.get_table_row_values(idx, self.tab_name_data)
        if not userdata:  # None or Empty
            self.glogger.error("Failed to get user Data %s", idx)
            return 0.0  # Error
        cur_status = userdata[self.col_name_statusflag]
        if cur_status != self.status_flag_withdrawal_pending:
            self.glogger.error(
                "The status flag (idx=%s) is not withdrawal-pending (%s). No money is in transaction now", idx,
                cur_status)
            return 0.0  # Error
        amount = float(userdata[self.col_name_transferamount])
        if amount >= 0.0:
            self.glogger.error("Invalid amount: idx=%s shareprice=%s amount=%f", idx, share_price, amount)
            return 0.0  # Error
        data_dict = {}
        num_shares_str, new_fmv_str = self._calc_num_shares_after_transaction(share_price,
                                                                              userdata[self.col_name_transferamount],
                                                                              userdata[self.col_name_numshares])
        data_dict[self.col_name_numshares] = num_shares_str
        data_dict[self.col_name_fair_market_value] = new_fmv_str
        data_dict[self.col_name_transferamount] = "0.0"
        data_dict[self.col_name_statusflag] = self.status_flag_active  # Active
        result = self._update_userdata_values(idx, data_dict)
        if not result:
            self.glogger.error("Failed to complete the withdrawal: idx=%s amount=%s shareprice=%s", idx,
                               userdata[self.col_name_transferamount], share_price)
            return 0.0  # Error
        return amount

    # --------------------------------------------------
    # Add money to the user (Fee < 0 or dividend > 0 )
    # --------------------------------------------------
    def add_money(self, idx: str, amount: float, share_price: float):
        userdata = self.get_table_row_values(idx, self.tab_name_data)
        if not userdata:  # None or Empty
            self.glogger.error("Failed to get user Data %s", idx)
            return 0.0  # Error

        cur_fund_str = userdata[self.col_name_fund]
        try:
            cur_fund = float(cur_fund_str)
        except Exception as err:
            self.glogger.error("The fund in the db (idx=%s) is not a float number:%s err=%s", idx, cur_fund_str, err)
            return 0.0  # Error

        self.glogger.debug("The user's (%s) fund is going to change from %f to %f", idx, cur_fund, cur_fund + amount)
        cur_fund += amount
        num_shares_str, new_fmv_str = self._calc_num_shares_after_transaction(share_price,
                                                                              str(amount),
                                                                              userdata[self.col_name_numshares])

        data_dict = {}
        data_dict[self.col_name_numshares] = num_shares_str
        data_dict[self.col_name_fair_market_value] = new_fmv_str
        data_dict[self.col_name_fund] = str(cur_fund)
        result = self._update_userdata_values(idx, data_dict)
        if not result:
            self.glogger.error("Failed to add mony: idx=%s amount=%s shareprice=%s", idx, amount, share_price)
            return 0.0  # Error
        return amount

    # ------------------------------------------
    # Calculate the
    # ------------------------------------------
    def _calc_num_shares_after_transaction(self, share_price: float, amount_str: str, cur_num_shares_str: str) -> (
            str, str):
        try:
            amount = float(amount_str)
            cur_num_shares = float(cur_num_shares_str)
            new_shares = amount / share_price
            cur_num_shares += new_shares
            num_shares_str = str(cur_num_shares)
            new_fmv = cur_num_shares * share_price
            new_fmv_str = str(new_fmv)
        except Exception as err:
            self.glogger.error("Invalid format in one of the values: shareprice=%s amount=%s num_shares=%s err=%s",
                               str(share_price), amount_str, cur_num_shares_str, err)
            return cur_num_shares_str, "0.0"
        return num_shares_str, new_fmv_str

    # ------------------------------------------
    # Get All Parent IDs
    # ------------------------------------------
    def get_all_parentids(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_data,
                                                      [self.col_name_userid, self.col_name_parentid])
        # print(value_list)
        return value_list

    # ------------------------------------------
    # Get the users that have no parent
    # ------------------------------------------
    def get_all_orphan_users(self):
        orphans = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_parentid, self.no_parent)
        # user_list = self.get_all_parentids()
        # orphans = []
        # for user_info in user_list:
        #    print(user_info[1])
        #    if user_info[1] == self.no_parent:
        #        orphans.append(user_info[0])
        return orphans

    # --------------------------------------------------
    # Get the users that belong to a specified parent
    # --------------------------------------------------
    def get_my_children(self, parentid: str):
        children = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_parentid, parentid)
        # user_list = self.get_all_parentids()
        # children = []
        # for user_info in user_list:
        #    #print(user_info[1])
        #    if user_info[1] == parentid:
        #        children.append(user_info[0])
        return children

    # ------------------------------------------
    # Get All account IDs
    # ------------------------------------------
    def get_all_accountids(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_data,
                                                      [self.col_name_userid, self.col_name_accountid])
        # print(value_list)
        return value_list

    # ------------------------------------------
    # Get All Status Flags
    # ------------------------------------------
    def get_all_statuses(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_data,
                                                      [self.col_name_userid, self.col_name_statusflag])
        # print(value_list)
        return value_list

    # ---------------------------------------------------------------
    # Calculate sum of shares and death probability (steps 1 & 2)
    # ---------------------------------------------------------------
    def _calc_sum_shares_dp(self, all_users_values: list) -> (float, float):
        dp_sum = 0.0
        shares_sum = 0.0
        for values in all_users_values:
            # print(values)
            try:
                idx = values[0]
                age = int(values[1])
                sex = values[2]
                numshares = float(values[3])
                statusflag = values[4]
                dp = dp_get_probability(age, sex)
            except Exception as err:
                self.glogger.error("Invalid format in one of the values: %s, err=%s", str(values), err)
                return 0.0, 0.0
            self.glogger.debug("idx=%s age=%d sex=%s num_shares=%f statusflag=%s dp=%f", idx, age, sex, numshares,
                               statusflag, dp)
            if statusflag == self.status_flag_closed:
                continue  # skip closed
            if statusflag == self.status_flag_deceased:
                continue  # skip deceased
            if statusflag == self.status_flag_closed:
                continue  # skip closed
            dp_sum += dp
            shares_sum += numshares
        # print(value_list)
        self.glogger.info("dp_sum=%f shares_sum=%f", dp_sum, shares_sum)
        return dp_sum, shares_sum

    # ------------------------------------------------
    # Normalize Number of shares and DPs (steps 3 & 4)
    # ------------------------------------------------
    def _normalize_shares_dp(self, distribute_num_shares: float, all_users_values: list, dp_sum: float,
                             shares_sum: float) -> list:
        total_shares_per_dp = 0.0
        transfer_list = []
        user_inx = 0
        for values in all_users_values:
            # print(values)
            try:
                idx = values[0]
                age = int(values[1])
                sex = values[2]
                numshares = float(values[3])
                statusflag = values[4]
                dp = dp_get_probability(age, sex)
            except Exception as err:
                self.glogger.error("Invalid format in one of the values: %s, err=%s", str(values), err)
                return None
            if statusflag == self.status_flag_deceased:
                continue  # skip deceased
            if statusflag == self.status_flag_closed:
                continue  # skip closed
            normalized_dp = dp / dp_sum
            # self.glogger.info("idx=%s normalized_dp=%f dp=%f dp_sum=%f", idx, normalized_dp, dp, dp_sum)
            normalized_num_shares = numshares / shares_sum
            shares_per_dp = normalized_dp * normalized_num_shares
            total_shares_per_dp += shares_per_dp
            transfer_val = [None] * 2
            transfer_val[0] = idx
            transfer_val[1] = shares_per_dp
            transfer_list.append(transfer_val)  # Add this to the array of values
            self.glogger.info("idx=%s normalized_dp=%f normalized_num_shares=%f shares_per_dp=%f",
                              idx, normalized_dp, normalized_num_shares, shares_per_dp)
        total_shares_transfer_percent = 0.0
        total_shares_transfer = 0.0
        for transfer_val in transfer_list:
            shares_per_dp = transfer_val[1]
            transfer_shares_percent = shares_per_dp / total_shares_per_dp
            total_shares_transfer_percent += transfer_shares_percent
            transfer_shares = transfer_shares_percent * distribute_num_shares
            total_shares_transfer += transfer_shares
            transfer_val[1] = transfer_shares  # place it in the array
            self.glogger.info("%s", str(transfer_val))
        self.glogger.info("total_shares_per_dp=%f total_shares_transfer=%f total_shares_transfer_percent=%f ",
                          total_shares_per_dp, total_shares_transfer, total_shares_transfer_percent)
        return transfer_list

    # ------------------------------------------
    # Distribute shares of a dead user
    # ------------------------------------------
    def calculate_dead_user_shares_distribution(self, idx: str) -> list:
        distribute_num_shares = self.get_num_shares(idx)
        if distribute_num_shares <= 0.0:
            self.glogger.error("The user %s has no shares or error", idx)
            return None
        status_flag = self.get_status_flag(idx)
        if status_flag != self.status_flag_deceased:
            self.glogger.error("The status of the user %s is not deceased (it is %s). Cannot distribute its shares",
                               idx, status_flag)
            return None

        all_users_values = self.get_table_data_per_colnames(self.tab_name_data, [self.col_name_userid,
                                                                                 self.col_name_age,
                                                                                 self.col_name_sex,
                                                                                 self.col_name_numshares,
                                                                                 self.col_name_statusflag])
        dp_sum, shares_sum = self._calc_sum_shares_dp(all_users_values)
        if dp_sum == 0.0 or shares_sum == 0.0:
            self.glogger.error("Failed to calculate DP-SUM or SHARES-SUM")
            return None

        transfer_list = self._normalize_shares_dp(distribute_num_shares, all_users_values, dp_sum, shares_sum)
        if not transfer_list:
            self.glogger.error("Failed to normalize DP and Shares of the users")
            return None
        return transfer_list

    # ------------------------------------------
    # Get all records with a specific flag value
    # ------------------------------------------
    def _get_all_specific_statusflag(self, status_flag_value: str):
        status_list = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_statusflag, status_flag_value)
        return status_list

    # ------------------------------------------
    # Get all records with a specific flag value
    # ------------------------------------------
    def get_all_statusflag_pending(self):
        return self._get_all_specific_statusflag(self.status_flag_pending)

    def get_all_statusflag_active(self):
        return self._get_all_specific_statusflag(self.status_flag_active)

    def get_all_statusflag_transfer(self):
        return self._get_all_specific_statusflag(self.status_flag_transfer)

    def get_all_statusflag_transfer_complete(self):
        return self._get_all_specific_statusflag(self.status_flag_transfer_complete)

    def get_all_statusflag_purchase_pending(self):
        return self._get_all_specific_statusflag(self.status_flag_purchase_pending)

    def get_all_statusflag_withdrawal(self):
        return self._get_all_specific_statusflag(self.status_flag_withdrawal)

    def get_all_statusflag_withdrawal_pending(self):
        return self._get_all_specific_statusflag(self.status_flag_withdrawal_pending)

    def get_all_statusflag_deceased(self):
        return self._get_all_specific_statusflag(self.status_flag_deceased)

    def get_all_statusflag_closed(self):
        return self._get_all_specific_statusflag(self.status_flag_closed)

    def get_all_statusflag_transfer_cancel(self):
        return self._get_all_specific_statusflag(self.status_flag_transfer_cancel)

    # ------------------------------------------
    # Get All  FMVs
    # ------------------------------------------
    def get_all_fmvs(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_data,
                                                      [self.col_name_userid, self.col_name_fair_market_value])
        # print(value_list)
        return value_list

    # ------------------------------------------
    # Get the number of shares
    # ------------------------------------------
    def get_num_shares(self, idx: str) -> float:
        num_shares_value_str = self.get_col_str_value(idx, self.tab_name_data, self.col_name_numshares)
        try:
            num_shares_value = float(num_shares_value_str)
        except Exception as err:
            self.glogger.error("The Num of shares in the db (idx=%s) is not a float number:%s err=%s", idx,
                               num_shares_value_str, err)
            return -1
        return num_shares_value

    # ------------------------------------------
    # Get the current FMV
    # ------------------------------------------
    def get_fmv(self, idx: str) -> float:
        fmv_value_str = self.get_col_str_value(idx, self.tab_name_data, self.col_name_fair_market_value)
        try:
            fmv_value = float(fmv_value_str)
        except Exception as err:
            self.glogger.error("The FMV in the db (idx=%s) is not a float number:%s err=%s", idx, fmv_value_str, err)
            return -1
        return fmv_value

    # ------------------------------------------
    # Update the FMV of the user
    # ------------------------------------------
    def _update_fmv(self, idx: str, share_price: float):
        userdata = self.get_table_row_values(idx, self.tab_name_data)
        if not userdata:  # None or Empty
            self.glogger.error("Failed to get user Data %s", idx)
            return False

        fund_value_str = userdata[self.col_name_fund]
        try:
            fund_value = float(fund_value_str)
        except Exception as err:
            self.glogger.error("The fund in the db (idx=%s) is not a float number:%s err=%s", idx, fund_value_str, err)
            return False

        num_shares_str = userdata[self.col_name_numshares]
        try:
            num_shares = float(num_shares_str)
        except Exception as err:
            self.glogger.error("The Num of shares in the db (idx=%s) is not a float number:%s err=%s", idx,
                               num_shares_str, err)
            return False
        if num_shares < 0:
            self.glogger.error("Failed to get the number of shared of user=%s", idx)
            return False

        current_fmv_str = userdata[self.col_name_fair_market_value]
        try:
            current_fmv = float(current_fmv_str)
        except Exception as err:
            self.glogger.error("The FMV in the db (idx=%s) is not a float number:%s fund_value=%f err=%s", idx,
                               current_fmv_str, fund_value, err)
            return False

        self.glogger.info("updating fmv: share_price=%f num_shares=%f current_fmv=%f", share_price, num_shares,
                          current_fmv)

        data_dict = {}
        new_fmv = num_shares * share_price
        dayprofit = new_fmv - current_fmv
        totprofit = new_fmv - fund_value
        data_dict[self.col_name_fair_market_value] = str(new_fmv)
        data_dict[self.col_name_dayprofit] = str(dayprofit)
        data_dict[self.col_name_totprofit] = str(totprofit)
        self.glogger.debug("Updating the FMV of idx=%s data_dict=%s", idx, str(data_dict))
        return self._update_userdata_values(idx, data_dict)

    # ------------------------------------------
    # Update FMV to all users
    # ------------------------------------------
    def update_all_fmvs(self, share_price: float):
        count_updates = 0
        idx_list = self.get_idx_list()
        for idx in idx_list:
            self.glogger.debug("Updating the FMV of idx=%s share_price=%s", idx, str(share_price))
            result = self._update_fmv(idx, share_price)
            if not result:
                self.glogger.error("Failed to update idx=%s share=%s", idx, str(share_price))
            else:
                count_updates += 1
        if count_updates == len(idx_list):
            return True
        return False

    # ------------------------------------------
    # Get the user's age
    # ------------------------------------------
    def get_age(self, idx: str) -> int:
        age_str = self.get_col_str_value(idx, self.tab_name_data, self.col_name_age)
        try:
            age = int(age_str)
        except Exception as err:
            self.glogger.error("The age in the db (idx=%s) is not an integer number:%s err=%s", idx, age_str, err)
            return -1
        return age

    # ------------------------------------------
    # Get All  totals
    # ------------------------------------------
    def get_all_totals(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_data,
                                                      [self.col_name_fair_market_value,
                                                       self.col_name_fund,
                                                       self.col_name_numshares,
                                                       self.col_name_numshares_from_inheritence,
                                                       self.col_name_transferamount,
                                                       ])
        # print(value_list)

        tot_fmv = 0.0
        tot_fund = 0.0
        tot_numshares = 0.0
        tot_numshare_from_inherit = 0.0
        tot_transfer = 0.0
        tot_deposit = 0.0
        tot_withdraw = 0.0
        totals = {}
        for rec in value_list:
            try:
                fmv = float(rec[0])
                fund = float(rec[1])
                numshares = float(rec[2])
                numshare_from_inherit = float(rec[3])
                transfer = float(rec[4])
            except Exception as err:
                self.glogger.error("One of the values in the db is not in the right format: %s err=%s", str(rec), err)
                return totals
            tot_fmv += fmv
            tot_fund += tot_fund
            tot_numshares += numshares
            tot_numshare_from_inherit += numshare_from_inherit
            tot_transfer += transfer
            if transfer < 0:
                tot_withdraw += transfer
            else:
                tot_deposit += transfer
        totals["tot_fmv"] = tot_fmv
        totals["tot_fund"] = tot_fund
        totals["tot_numshares"] = tot_numshares
        totals["tot_numshare_from_inherit"] = tot_numshare_from_inherit
        totals["tot_transfer"] = tot_transfer
        totals["tot_withdraw"] = tot_withdraw
        totals["tot_deposit"] = tot_deposit
        return totals

    # ------------------------------------------
    # Get All  contracts
    # ------------------------------------------
    def get_all_contracts(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_data, [self.col_name_userid,
                                                                           self.col_name_user_info])
        #print(value_list)
        contract_list = []
        for entry in value_list:
            try:
                rec = {}
                idx = entry[0]
                info = entry[1]
                info = json.loads(info)
                rec["idx"] = idx
                rec["contract_id"] = info["contract_id"]
                rec["advisor_id"] = info["advisor_id"]
                rec["email"] = info["email"]
                rec["funding"] = info["funding"]
                rec["payout_ages"] = info["payout_ages"]
                rec["signed_date"] = info["signed_date"]
                self.glogger.debug("rec=%s type(rec)=%s", rec, str(type(info)))
                contract_list.append(rec)
            except Exception as err:
                self.glogger.error("One of the values in the db is not in the right format: %s err=%s", str(rec), err)
                return contract_list
        return contract_list
