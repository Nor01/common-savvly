from datetime import datetime
from common.util.logging_helper import get_logger
from common.database.db_tablecollection import *

# -----------------------------------------------------------------------------------------------------------------------
# Transaction Table
# -----------------------------------------------------------------------------------------------------------------------
class DbInherited(DbTableCollection):
    tab_name_inherit = "inherited"  # User Inheritance
    col_name_timestamp = "idx"  # This is the primary key - must be "idx" - do not change it
    col_name_from_user = "from_idx"
    col_name_to_user = "to_idx"
    col_name_numshares = "numshares"
    col_name_shareprice = "shareprice"

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbInheritance")
        tables_info = self._build_tables_info()
        tables_attributes = self._build_tables_attributes()
        super().__init__(tables_info, tables_attributes)

    # ----------------------------------------------------------------------
    # Create the tables
    # ----------------------------------------------------------------------
    def _build_tables_info(self):
        tables_info = {}
        tables_info[self.tab_name_inherit] = [
            (self.col_name_timestamp, "text PRIMARY KEY"),
            (self.col_name_from_user, "text"),
            (self.col_name_to_user, "text"),
            (self.col_name_numshares, "text"),
            (self.col_name_shareprice, "text"),
        ]
        return tables_info

    # ----------------------------------------------------------------------
    # Create a dictionary of the tables attributes
    # ----------------------------------------------------------------------
    def _build_tables_attributes(self):
        tables_attributes = {}
        tables_attributes[self.tab_name_inherit] = { "create" : "CLUSTERING ORDER BY (" + self.col_name_timestamp + " DESC)" }
        return tables_attributes

    # -----------------------------------
    # Add new inheritance record
    # -----------------------------------
    def add_new_inheritance(self, from_idx: str, to_idx: str, num_shares: float, share_price: float):
        primekey = self._build_primary_key()
        if self.add_new_idx(primekey) == False:
            return False
        values = {}
        values[self.col_name_from_user] = from_idx
        values[self.col_name_to_user] = to_idx
        values[self.col_name_numshares] = str(num_shares)
        values[self.col_name_shareprice] = str(share_price)
        self._update_inherited_values(primekey, values)

    # -----------------------------------------------------
    # Update user data in a specific table: inherited
    # -----------------------------------------------------
    def _update_inherited_values(self, idx: str, data_dict: dict):
        return self.update_values(idx, self.tab_name_inherit, data_dict)

    # -----------------------------------
    # build DateTime
    # -----------------------------------
    def _build_primary_key(self):
        today = datetime.now()
        primekey = today.strftime("%Y%m%d%H%M%S%f")[:-3]
        return primekey