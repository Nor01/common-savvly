from common.util.logging_helper import get_logger
from common.controllers.dbhandles import *

# -----------------------------------------------------------------------------------------------------------------------
# This class handles dividends
# -----------------------------------------------------------------------------------------------------------------------
class Dividend:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("Dividend")
        dbh = Dbhandles.get_instance()
        self.usertable = dbh.get_usertables()
        self.trtable = dbh.get_transactiontable()

    # ----------------------------------------------------------------------------
    # Deduct a fee
    # ----------------------------------------------------------------------------
    def add_dividend(self, idx: str, amount: float, shareprice: float):
        self.glogger.info("Adding Dividend - idx=%s amount=%f shareprice=%s", idx, amount, shareprice)
        amount = self.usertable.add_money(idx, amount, shareprice)
        if amount == 0:
            return False
        return self.trtable.add_new_transaction(idx, DbTransactions.tran_type_dividends, amount, shareprice)