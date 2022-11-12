from common.util.logging_helper import get_logger
from common.controllers.dbhandles import *


# -----------------------------------------------------------------------------------------------------------------------
# This class handles money Transfer (Deposit & Withdraw)
# -----------------------------------------------------------------------------------------------------------------------
class MoneyTransfer:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("MoneyTransfer")
        dbh = Dbhandles.get_instance()
        self.usertable = dbh.get_usertables()
        self.trtable = dbh.get_transactiontable()

   # ----------------------------------------------------------------------------
    # Deposit money to the account - Called by the user (Front End)
    # ----------------------------------------------------------------------------
    def deposit_money(self, idx: str, amount: float, transactid:str):   return self.usertable.deposit_money(idx, amount, transactid)

    # ----------------------------------------------------------------------------
    # Set Deposit (transfer) Complete - Called by Bank-adaptor
    # ----------------------------------------------------------------------------
    def set_transfer_complete(self, idx: str): return self.usertable.set_transfer_complete(idx)

    # ----------------------------------------------------------------------------
    # Set purchase status flags-> Pending  - Called by Trader
    # ----------------------------------------------------------------------------
    def set_purchase_pending(self, idx: str):   return self.usertable.set_statusflag_purchase_pending(idx)

    # ----------------------------------------------------------------------------
    # Set Purchase Complete  - Called by Trader
    # ----------------------------------------------------------------------------
    def set_purchase_complete(self, idx: str, shareprice: float):
        amount = self.usertable.set_purchase_complete(idx, shareprice)
        if amount == 0:
            return False
        return self.trtable.add_transaction_money_transfer(idx, amount, shareprice)

    # ----------------------------------------------------------------------------
    # Withdrawal money from the account - Called by the user (Front End)
    # ----------------------------------------------------------------------------
    def withdrawal_money(self, idx:str, amount:float):  return self.usertable.withdrawal_money(idx, amount)

    # ----------------------------------------------------------------------------
    # Set withdrawal status flags-> Pending  - Called by Bank-adaptor
    # ----------------------------------------------------------------------------
    def set_withdrawal_pending(self, idx: str):   return self.usertable.set_statusflag_withdrawal_pending(idx)

    # ----------------------------------------------------------------------------
    # Set withdrawal Complete  - Called by Trader
    # ----------------------------------------------------------------------------
    def set_withdrawal_complete(self, idx: str, shareprice: float):
        amount = self.usertable.set_withdrawal_complete(idx, shareprice)
        if amount == 0:
            return False
        return self.trtable.add_transaction_money_transfer(idx, amount, shareprice)

    # ------------------------------------------
    # Get all records with a specific flag value
    # ------------------------------------------
    def get_all_statusflag_transfer(self):           return self.usertable.get_all_statusflag_transfer()
    def get_all_statusflag_transfer_complete(self):  return self.usertable.get_all_statusflag_transfer_complete()
    def get_all_statusflag_purchase_pending(self):   return self.usertable.get_all_statusflag_purchase_pending()
    def get_all_statusflag_withdrawal(self):         return self.usertable.get_all_statusflag_withdrawal()
    def get_all_statusflag_withdrawal_pending(self): return self.usertable.get_all_statusflag_withdrawal_pending()





