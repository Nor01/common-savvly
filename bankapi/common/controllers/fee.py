from common.util.logging_helper import get_logger
from common.controllers.dbhandles import *

# -----------------------------------------------------------------------------------------------------------------------
# This class handles fee deductions
# -----------------------------------------------------------------------------------------------------------------------
class Fee:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("Fee")
        dbh = Dbhandles.get_instance()
        self.usertable = dbh.get_usertables()
        self.trtable = dbh.get_transactiontable()

    # ----------------------------------------------------------------------------
    # Deduct a management fee
    # ----------------------------------------------------------------------------
    def deduct_management_fee(self, idx: str, amount: float, shareprice: float):
        return self._deduct_fee(idx, DbTransactions.tran_type_management_fee, amount, shareprice)

    # ----------------------------------------------------------------------------
    # Deduct a sign-up fee
    # ----------------------------------------------------------------------------
    def deduct_signup_fee(self, idx: str, amount: float, shareprice: float):
        return self._deduct_fee(idx, DbTransactions.tran_type_sign_up_fee, amount, shareprice)

    # ----------------------------------------------------------------------------
    # Deduct a MISC fee
    # ----------------------------------------------------------------------------
    def deduct_misc_fee(self, idx: str, amount: float, shareprice: float):
        return self._deduct_fee(idx, DbTransactions.tran_type_misc_fee, amount, shareprice)

    # ----------------------------------------------------------------------------
    # Deduct a fee
    # ----------------------------------------------------------------------------
    def _deduct_fee(self, idx: str, fee_type: str, amount: float, shareprice: float):
        self.glogger.info("Fee deduction - idx=%s type=%s amount=%f shareprice=%s", idx, fee_type, amount, shareprice)
        amount = self.usertable.add_money(idx, amount, shareprice)
        if amount == 0:
            return False
        return self.trtable.add_new_transaction(idx, fee_type, amount, shareprice)