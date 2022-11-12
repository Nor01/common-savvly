from datetime import datetime
from common.util.logging_helper import get_logger
from common.database.db_tablecollection import *

# -----------------------------------------------------------------------------------------------------------------------
# Transaction Table
# -----------------------------------------------------------------------------------------------------------------------
class DbTransactions(DbTableCollection):
    tab_name_tran = "transactions"

    col_name_timestamp = "idx"  # This is the primary key - must be "idx" - do not change it
    col_name_userid = "userid"  # the user ID (OID)
    col_name_transaction_type = "tran_type"
    col_name_amount = "amount"
    col_name_numshares = "numshares"
    col_name_shareprice = "shareprice"

    tran_type_deposit = "deposit"
    tran_type_withdrawal = "withdrawal"
    tran_type_dividends = "dividends"
    tran_type_management_fee = "management_fee"
    tran_type_sign_up_fee = "sign_up_fee"
    tran_type_misc_fee = "misc_fee"
    tran_types = [tran_type_deposit, tran_type_withdrawal, tran_type_dividends,tran_type_management_fee,  tran_type_sign_up_fee, tran_type_misc_fee]

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbTransactions")
        tables_info = self._build_tables_info()
        tables_attributes = self._build_tables_attributes()
        super().__init__(tables_info, tables_attributes)

    # ----------------------------------------------------------------------
    # Create all user data tables
    # ----------------------------------------------------------------------
    def _build_tables_info(self):
        tables_info = {}

        tables_info[self.tab_name_tran] = [
            (self.col_name_timestamp, "text PRIMARY KEY"),
            (self.col_name_userid, "text"),
            (self.col_name_transaction_type, "text"),
            (self.col_name_amount, "text"),
            (self.col_name_numshares, "text"),
            (self.col_name_shareprice, "text"),
        ]

        return tables_info

    # ----------------------------------------------------------------------
    # Create a dictionary of the tables attributes
    # ----------------------------------------------------------------------
    def _build_tables_attributes(self):
        tables_attributes = {}
        tables_attributes[self.tab_name_tran] = { "create" : "CLUSTERING ORDER BY (" + self.col_name_timestamp + " DESC)" }
        return tables_attributes

    # -----------------------------------
    # Add a new transaction
    # -----------------------------------
    def add_new_transaction(self, idx: str, tran_type : str, amount: float, shareprice: float):
        if not tran_type in self.tran_types:
            self.glogger.error("Invalid transaction type: %s", tran_type)
            pass # Nevertheless continue

        num_shares = amount/shareprice # Assume the number of shares is not an integer
        primekey = self._build_primary_key()
        if self.add_new_idx(primekey) == False:
            return False
        values = {}
        values[self.col_name_userid] = idx
        values[self.col_name_transaction_type] = tran_type
        values[self.col_name_amount] = str(amount)
        values[self.col_name_numshares] = str(num_shares)
        values[self.col_name_shareprice] = str(shareprice)
        return self.update_values(primekey, self.tab_name_tran, values)

    # --------------------------------------------------------------
    # Add transaction of type Money Transfer (deposit/withdrawal)
    # --------------------------------------------------------------
    def add_transaction_money_transfer(self, idx: str, amount: float, shareprice: float):
        if amount < 0:
            result = self.add_new_transaction(idx, self.tran_type_withdrawal, amount, shareprice)
        else:
            result = self.add_new_transaction(idx, self.tran_type_deposit, amount, shareprice)
        return result

    # ------------------------------------------
    # Get all Transactions
    # ------------------------------------------
    def get_all_transactions(self) -> list:
         return self.get_rows_specific_col_value(self.tab_name_tran, self.col_name_userid, idx)

    # ------------------------------------------
    # Get All Transactions
    # ------------------------------------------
    def get_all_amounts(self) -> list:
        value_list = self.get_table_data_per_colnames(self.tab_name_tran, [self.col_name_timestamp,
                                                                           self.col_name_userid,
                                                                           self.col_name_amount])
        #print(value_list)
        return value_list

    # ------------------------------------------
    # Get Transactions of a specific user
    # ------------------------------------------
    def get_user_values(self, idx:str) -> list:
         return self.get_rows_specific_col_value(self.tab_name_tran, self.col_name_userid, idx)

    # ------------------------------------------
    # Sum up User amounts
    # ------------------------------------------
    def get_total_user_amounts(self, idx:str) -> float:
        total = 0.0
        value_list = self.get_user_values(idx)
        for value_dict in  value_list:
            try:
                amount = value_dict[self.col_name_amount]
                total += float(amount)
            except Exception as err:
                self.glogger.error("Failed to get the amount of the: %s", str(value_dict))
                return total
        return total

    # ------------------------------------------
    # Sum up User shares
    # ------------------------------------------
    def get_total_user_shares(self, idx:str) -> float:
        total = 0.0
        value_list = self.get_user_values(idx)
        for value_dict in  value_list:
            try:
                amount = value_dict[self.col_name_numshares]
                total += float(amount)
            except Exception as err:
                self.glogger.error("Failed to get the number of shares of the: %s", str(value_dict))
                return total
        return total

    # -----------------------------------------------------
    # Update user data in a specific table: transactions
    # -----------------------------------------------------
    #def _update_transactions_values(self, idx: str, data_dict: dict):
    #    return self.update_values(idx, self.tab_name_tran, data_dict)

    # -----------------------------------
    # build DateTime
    # -----------------------------------
    def _build_primary_key(self):
        today = datetime.now()
        primekey =  today.strftime("%Y%m%d%H%M%S%f")[:-3]
        return primekey