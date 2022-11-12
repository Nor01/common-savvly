import time
import ast
# from common.util.logging_helper import get_logger
# from common.util.datetime_parser import datetime_parse, datetime_calc_age
from common.database.db_tablecollection import *
from common.kv.kv_wrapper import AzureKeyVaultWrapper
# from common.util.string_helper import hash256
from common.models.dbusertables import DbUserTables
from common.models.deathprobability import dp_get_probability


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
# RIA table [idx, crd, associated, last_update] rest of personal details are stored in the Active directory
#
class DbRIATables(DbTableCollection):
    tab_name_data = "riadata"  # RIA data Table

    col_name_ria_id = "idx"  # User ID (provided as OID by Active Directory)
    col_name_CRD_number = "crd"  # RIA CRD number
    col_name_associated_RIA = "associated"  # Associated RIA
    col_name_lastupdate = "lastupdate"

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
    def _build_tables_info(self):
        tables_info = {}

        tables_info[self.tab_name_data] = [
            (self.col_name_ria_id, "text PRIMARY KEY"),
            (self.col_name_CRD_number, "text"),
            (self.col_name_associated_RIA, "text"),
            (self.col_name_lastupdate, "text"),
        ]

        return tables_info

    # -----------------------------------
    # Add new RIA
    # -----------------------------------
    def add_new_RIA(self, idx: str, crd: str, associated: str):
        self.glogger.info("Adding IDX=%s CRD=%s associated=%s", idx, crd, associated)

        if self.add_new_idx(idx) == False:
            return False

        values = {
            self.col_name_CRD_number: crd,
            self.col_name_associated_RIA: associated,
            self.col_name_lastupdate: self._get_last_update_time()
        }
        self.update_values(idx, self.tab_name_data, values)

        return True

    # -----------------------------------------------------------------------------------------------------------------------
    # is_RIA (idx)
    # -----------------------------------------------------------------------------------------------------------------------
    def is_RIA(self, idx: str):
        ret = self.get_col_str_value(idx, self.tab_name_data, self.col_name_CRD_number)
        if ret is None:
            self.glogger.error("Failed to check if the ID=%s is a RIA. Apparently is not an RIA", idx)
            return False
        self.glogger.info("id=%s is a RIA", idx)
        return True

    # -----------------------------------------------------------------------------------------------------------------------
    # get_RIA_info (idx)
    # -----------------------------------------------------------------------------------------------------------------------
    def get_RIA_info(self, idx: str):
        ret = self.get_table_row_values(idx, self.tab_name_data)
        self.glogger.info(f"get_RIA_info IDX={idx} is {ret}")
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
    @staticmethod
    def _get_last_update_time():
        return str(int(time.time()))

    # --------------------------------------------------
    # Get the users that belong to a specified associated
    # --------------------------------------------------
    def get_all_associated_RIAs(self, associated: str):
        children = self.get_rows_specific_col_value(self.tab_name_data, self.col_name_associated_RIA, associated)
        return children

    # --------------------------------------------------
    # get_RIA_children Get the users that belong to a specified RIA
    # --------------------------------------------------
    @staticmethod
    def get_RIA_children(idx: str):
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
