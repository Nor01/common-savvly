from common.util.utility_functions import utils_is_dev_env
from common.util.logging_helper import get_logger
from bankapi.models.treasurywrapper import *
from common.controllers.moneytransfer import *

# -----------------------------------------------------------------------------------------------------------------
# Bank API
# -----------------------------------------------------------------------------------------------------------------
class BankAPI:
    __instance = None

    ## ---------------------------------------------
    ## Return the singletone object
    ## ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if BankAPI.__instance is None:
            BankAPI()
        return BankAPI.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
        if BankAPI.__instance != None:
            raise Exception("This class is a singleton!")
            return
        BankAPI.__instance = self
        self.glogger = get_logger("BankAPI")
        if utils_is_dev_env():
            corp_key = "key_1g0xjb9yg0t_sandbox_001"
            corp_secret = "aFy6Yff992gLiZv673b8Kvfnlwq467Or"
            savvly_key = "key_1g0xjb9yg0t_sandbox_004"
            savvly_secret = "37gf9hviAyVOjMqoaEsdqKW0atoMgMRR"
        else:
            corp_key = "key_1g0xjb9yg0t_sandbox_001"             # To be updated
            corp_secret = "aFy6Yff992gLiZv673b8Kvfnlwq467Or"     # To be updated
            savvly_key = "key_1g0xjb9yg0t_sandbox_004"           # To be updated
            savvly_secret = "37gf9hviAyVOjMqoaEsdqKW0atoMgMRR"   # To be updated
        corp_callback_web_url = "https://savvly-dev-api.azurewebsites.net/bankapihook_corp"
        savvly_callback_web_url = "https://savvly-dev-api.azurewebsites.net/bankapihook_savvly"
        self.corporate_account = TreasuryWrapper(corp_key, corp_secret, corp_callback_web_url)
        self.savvly_account = TreasuryWrapper(savvly_key, savvly_secret, savvly_callback_web_url)

    # ---------------------------------------------
    # Get the list of the transactions in the bank
    # ---------------------------------------------
    def process_users_transactions(self):
        bank_trans_list = self.savvly_account.get_deposit_transactions()
        if bank_trans_list is None:
            return
        moneytr = MoneyTransfer()
        user_trans_list = moneytr.get_all_statusflag_transfer()
        if user_trans_list is None:
            return
        self.glogger.info("There are %d deposit-transactions in the bank, and %d transfers by the user", len(bank_trans_list), len(user_trans_list))
        #print(bank_trans_list)
        #print(user_trans_list)
        matched_transactions = []
        for user_trans in user_trans_list:
            bank_trans = self._find_user_transfer_in_bank_transactions(user_trans, bank_trans_list)
            if bank_trans is None:
                self.glogger.info("The user (%s) has reported on a money-transfer, but the transaction does not appear in the bank", str(user_trans))
                continue
            #print(user_trans)
            #print(bank_trans)
            try:
                user_amount = float(user_trans["transferamount"])
                bank_amount = float(bank_trans["amount"])
                if user_amount != bank_amount:
                    self.glogger.info("The amount of money that the user has reported (%s) does not match the one appear in the bank (%s), bank=%s user=%s",
                                      str(user_amount), str(bank_amount), str(bank_trans), str(user_trans))
                    continue
            except Exception as err:
                self.glogger.info("Something is wrong in the format of the transactions bank=%s user=%s", str(bank_trans), str(user_trans))
                continue
            self.glogger.debug("Transaction found bank=%s user=%s", str(bank_trans), str(user_trans))
            new_dict = user_trans.copy()
            new_dict["bank_trans"]  = bank_trans
            matched_transactions.append(new_dict)
            moneytr.set_transfer_complete(user_trans["idx"])  # MNark that the transfer completed
        return matched_transactions

    # ----------------------------------------------------------------
    # Find a user transaction in the list of bank transactions
    # ----------------------------------------------------------------
    def _find_user_transfer_in_bank_transactions(self, user_trans : dict, bank_trans_list : list) -> dict:
        user_trans_id = user_trans["transferid"]
        for bank_trans in bank_trans_list:
            self.glogger.debug("Looking for transaction-id=%s in the transaction list. Current Rec=%s",user_trans_id, str(bank_trans))
            bank_trans_id = bank_trans["tran_id"]
            if not user_trans_id == bank_trans_id:
                self.glogger.debug("No Match user_trans_id=%s bank_trans_id=%s", user_trans_id, bank_trans_id)
                continue
            self.glogger.info("Match user_trans_id=%s bank_trans_id=%s", user_trans_id, bank_trans_id)
            return bank_trans
        return None

    # ---------------------------------------------
    # Get the Corporate/Savvly Object
    # ---------------------------------------------
    def get_corporate_object(self):   return self.corporate_account
    def get_savvly_object(self):      return self.savvly_account