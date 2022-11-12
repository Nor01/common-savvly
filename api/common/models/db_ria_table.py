import time
import ast
# from common.util.logging_helper import get_logger
# from common.util.datetime_parser import datetime_parse, datetime_calc_age
from pydantic import ValidationError
from common.database.db_tablecollection import *
from common.kv.kv_wrapper import AzureKeyVaultWrapper
# from common.util.string_helper import hash256
from common.models.dbusertables import DbUserTables
from common.models.deathprobability import dp_get_probability
from common.models.advisor_info_schema import AdvisorInfoScheme
from common.util.utility_functions import *


# todo : functions
# del_RIA (idx) do we need to del his clients as well?
# get_all_specific_statusflag (idx, statusflag) (multiple functions, same as in users )


#
# -----------------------------------------------------------------------------------------------------------------------
# RIA Data
# -----------------------------------------------------------------------------------------------------------------------


#
# from slide:
# Full RIA registration (name, last name, address, phone, email, CRD number, Associated RIA)
#
# RIA table [idx, crd, crd_firm, associated, advisorinfo, last_update] rest of personal details are stored in the Active directory
#
class DbRIATables(DbTableCollection):
    tab_name_data = "riadata"  # RIA data Table

    col_name_advisor_id = "idx"  # User ID (provided as OID by Active Directory)
    col_name_CRD_individual = "crdindividual"  # Advisor's individual CRD number
    col_name_CRD_firm = "crdfirm"  # Advisor's firm CRD number
    col_name_associated_RIA = "associated"  # Associated RIA
    col_name_advisor_info = "advisorinfo"  # Advisor info
    col_name_lastupdate = "lastupdate"
    col_name_validated = "isvalidated"

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbRIATables")
        tables_info = self._build_tables_info()
        super().__init__(tables_info)

    # ----------------------------------------------------------------------
    # Create all RIA data tables
    # ----------------------------------------------------------------------
    # noinspection PyDictCreation
    def _build_tables_info(self):
        tables_info = {}

        tables_info[self.tab_name_data] = [
            (self.col_name_advisor_id, "text PRIMARY KEY"),
            (self.col_name_CRD_individual, "text"),
            (self.col_name_CRD_firm, "text"),
            (self.col_name_associated_RIA, "text"),
            (self.col_name_advisor_info, "text"),
            (self.col_name_lastupdate, "text"),
            (self.col_name_validated, "text"),
        ]

        return tables_info

    # -----------------------------------
    # Add new Advisor
    # -----------------------------------
    def add_new_advisor(self, idx: str, crd_individual: str, crd_firm: str, associated: str, advisor_info: dict):

        try:
            utils_add_creation_time_to_dic(advisor_info)  # Add creation time to the dictionary
            advisor_info_validated = AdvisorInfoScheme(**advisor_info)
        except ValidationError as e:
            self.glogger.error(f"Data {advisor_info} validation failed {e.json()}")
            return False

        self.glogger.info(
            f"Adding IDX={idx} CRD_individual={crd_individual} CRD_firm={crd_firm} associated={associated} info={advisor_info}")

        if crd_individual is None and crd_firm is None:
            self.glogger.error(f"At least one CRD number required")
            return False

        if not self.add_new_idx(idx):
            return False

        values = {
            self.col_name_CRD_individual: crd_individual,
            self.col_name_CRD_firm: crd_firm,
            self.col_name_associated_RIA: associated,
            self.col_name_advisor_info: advisor_info_validated.json(),
            self.col_name_lastupdate: utils_get_current_epoch_time(),
            self.col_name_validated: 'true',     # Assume it is not validated yet - @todo  TBD - change to 'false'
        }
        self.update_values(idx, self.tab_name_data, values)

        return True

    # -----------------------------------------------------------------------------------------------------------------------
    # Get the advisor type: ValidatedAdvisor or NoValidatedAdvisor
    # -----------------------------------------------------------------------------------------------------------------------
    def _get_advisor_type(self, idx: str):
        advisor_type = None
        dic = self.get_table_row_values(idx, self.tab_name_data)
        if dic is None or len(dic) == 0:
            self.glogger.info("Failed to check if the ID=%s is an advisor. Apparently is not an advisor", idx)
            return None # This is not an advisor
        try:
            self.glogger.info("AdvisorType: Row=%s type=%s", dic, str(type(dic)))
            #is_validated = dic[self.col_name_validated]
            is_validated = 'true'
            is_validated = is_validated.lower()
            if is_validated == "true":
                advisor_type = "validatedadvisor"
            elif is_validated == "false":
                advisor_type = "advisor"
            else:
                self.glogger.error("Invalid advisor type found in the DB. It should be either true or flase. idx=%s", idx)
                return None  # This is not an advisor
        except Exception as err:
            self.glogger.error("Exception to check if the advisor %s is validated. err=%s", idx, err)
            return None  # This is not an advisor
        self.glogger.info("id=%s is an advisor of type: %s", idx, advisor_type)
        return advisor_type

    # -----------------------------------------------------------------------------------------------------------------------
    #Is this an advisor and what type
    # Returns two values:
    # value1: True (advisor) , False (not advisor)
    # value2: True(validated), false (not validated)
    # -----------------------------------------------------------------------------------------------------------------------
    def is_advisor(self, idx: str):
        advisor_type = self._get_advisor_type(idx)
        if advisor_type is None:
            return False, False   # Not advisor, of course not validated
        if advisor_type == "advisor":
            return True, False  # advisor, but not validated
        if advisor_type == "validatedadvisor":
            return True, True  # advisor, validated
        self.glogger.info("Invalid advisor type:%s for idx=%s", advisor_type, idx)
        return False, False # Error

    # -----------------------------------------------------------------------------------------------------------------------
    # is_advisor (idx)
    # -----------------------------------------------------------------------------------------------------------------------
    #def is_advisor(self, idx: str):
    #    ret = self.get_col_str_value(idx, self.tab_name_data, self.col_name_advisor_id)
    #    if ret is None:
    #        self.glogger.error("Failed to check if the ID=%s is an advisor. Apparently is not an advisor", idx)
    #        return False
    #    self.glogger.info("id=%s is an advisor", idx)
    #    return True

    # -----------------------------------------------------------------------------------------------------------------------
    # is_advisor_by_crd (crd_individual, crd_firm)
    # -----------------------------------------------------------------------------------------------------------------------
    def is_advisor_by_crd(self, crd_individual: str = None, crd_firm: str = None):
        if crd_individual is None and crd_firm is None:
            self.glogger.error("expect at least one crd number")
            return False
        ret_individual = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_CRD_individual,
                                                          crd_individual)
        ret_firm = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_CRD_firm, crd_firm)
        if ret_individual == [] and ret_firm == []:
            self.glogger.error(
                f"Failed to check if the CRD_individual={crd_individual}, CRD_firm={crd_firm} is an advisor. Apparently is not an advisor")
            return False

        if ret_individual != []:
            advisor_found = ret_individual[0]
        else:
            advisor_found = ret_firm[0]

        self.glogger.info(f"advisor found {advisor_found} ")
        return True

    # -----------------------------------------------------------------------------------------------------------------------
    # get_RIA_info (idx)
    # -----------------------------------------------------------------------------------------------------------------------
    def get_advisor_info(self, idx: str):
        ret = self.get_table_row_values(idx, self.tab_name_data)
        self.glogger.info(f"get_advisor_info IDX={idx} is {ret}")
        return ret

    # -----------------------------------------------------------------------------------------------------------------------
    # add_child (idx, userid)
    # -----------------------------------------------------------------------------------------------------------------------
    def add_child(self, idx: str, userid: str):
        userTable = DbUserTables()
        # need to check first if user exists
        if not userTable.is_active_user(userid):
            self.glogger.info(f"User {userid} not found")
            return False
        return userTable.set_parentid(userid, parentid=idx)

    # -----------------------------------------------------------------------------------------------------------------------
    # del_child (idx, userid)
    # -----------------------------------------------------------------------------------------------------------------------
    def del_child(self, userid: str):
        userTable = DbUserTables()
        # need to check first if user exists
        if not userTable.is_active_user(userid):
            self.glogger.info(f"User {userid} not found")
            return False
        return userTable.clear_parentid(userid)

    # -----------------------------------
    # Get the update time
    # -----------------------------------
    #@staticmethod
    #def _get_last_update_time():
    #    return str(int(time.time()))

    # --------------------------------------------------
    # Get the users that belong to a specified associated
    # --------------------------------------------------
    def get_all_associated_RIAs(self, associated: str):
        if associated == '*':
            children = self.get_all_rows(self.tab_name_data)
        else:
            children = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_associated_RIA, associated)
        return children

    # --------------------------------------------------
    # get_RIA_children Get the users that belong to a specified advisor
    # --------------------------------------------------
    @staticmethod
    def get_advisor_children(idx: str):
        userTable = DbUserTables()

        children = userTable.get_my_children(parentid=idx)
        return children

    # ------------------------------------------
    # Get all records with a specific flag value
    # ------------------------------------------
    @staticmethod
    def _get_all_specific_statusflag(idx: str, status_flag_value: str):
        userTable = DbUserTables()
        status_list = userTable.get_rows_specific_two_col_value(userTable.tab_name_data,
                                                                userTable.col_name_statusflag, status_flag_value,
                                                                userTable.col_name_parentid, idx)

        return status_list

    # -----------------------------------
    # Delete an existing adviso
    # -----------------------------------
    def delete_advisor(self, idx: str):
        return self.delete_record(idx)

    # --------------------------------------------------
    # Set advisor Validated: 'true' or 'false'
    # --------------------------------------------------
    def set_is_validated(self, idx: str, is_validated : str):
        is_validated = is_validated.lower()
        if is_validated.startswith('t'):
            is_validated = 'true'
        elif is_validated.startswith('f'):
            is_validated = 'false'
        else:
            self.glogger.error("Invalid paramater value passed to set advisor validated: %s (should be true or false)",is_validated)
            return False
        self.update_value(idx, self.tab_name_data, self.col_name_validated, is_validated)
        return True