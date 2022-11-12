import requests
import logging
from http.client import HTTPConnection  # py3
import datetime
from requests.auth import HTTPBasicAuth
#import pycurl
import json
#from io import BytesIO
from common.util.utility_functions import utils_is_dev_env
from common.util.logging_helper import get_logger

# -----------------------------------------------------------------------------------------------------------------
# Wrapper for the Treasury Prime API : https://developers.treasuryprime.com/docs/introduction
# -----------------------------------------------------------------------------------------------------------------
class TreasuryWrapper:
    ## ---------------------------------------------
    ## Operation Name
    ## ---------------------------------------------
    op_name_post    = "post"  # Post
    op_name_get     = "get"   # Get
    op_name_patch   = "patch"   # Patch
    op_name_delete  = "delete"   # Patch

    ## ---------------------------------------------
    ## API names
    ## ---------------------------------------------
    api_name_webhook = "webhook"             # Register for a webhook
    api_name_ping    = "ping"                # Ping the server
    api_name_account = "account"             # Ping the server
    api_name_transfer = "book"               #Transfer from one account to another
    api_name_transaction = "transaction"     #Returns a list of transactions across all accounts

    ## ---------------------------------------------
    ## Account Types
    ## ---------------------------------------------
    account_type_sweep       = "sweep"     # brokerage account that is linked to an investment account
    account_type_checking    = "checking"  # account that allows you to easily deposit and withdraw money
    account_type_savings     = "savings"   # savings account is an interest-bearing deposit account held at a bank

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self, api_key:str, api_secret:str, webhook_url : str):
        self.glogger = get_logger("TreasuryWrapper")
        self.key = api_key
        self.secret = api_secret
        self.callback_savvly_web_url = webhook_url
        log = logging.getLogger("urllib3")
        log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        log.addHandler(ch)
        HTTPConnection.debuglevel = 0    # print statements from `http.client.HTTPConnection` to console/stdout
        if utils_is_dev_env():
            self.url = "https://api.sandbox.treasuryprime.com"
        else:
            self.url = "https://api.treasuryprime.com"
        self.savvly_user_id          = "savvly"
        self.savvly_secret           = "secret"

        self._delete_all_webhooks()
        self._register_webhook("book.create")
        self._register_webhook("book.update")
        self._register_webhook("ach.create")
        self._register_webhook("ach.update")
        self._register_webhook("webhook.create")
        #self._register_webhook("webhook.delete")
        #self._register_webhook("webhook.update")

    # -----------------------------------
    # Get the API Info
    # -----------------------------------
    def get_api_info(self): return self._run_curl_interface(self.api_name_ping)

    # -----------------------------------
    # Get my account types and ids
    # -----------------------------------
    def get_account_ids(self) -> list:
        accounts = self._get_all_accounts()
        account_ids = []
        for account in accounts:
            rec = {}
            rec["account_type"] = account["account_type"]
            rec["id"] = account["id"]
            account_ids.append(rec)
        return account_ids

    # -----------------------------------
    # Get my accounts
    # -----------------------------------
    def get_checking_account(self) -> dict:  return self._get_specific_account(self.account_type_checking)
    def get_sweep_account(self) -> dict:     return self._get_specific_account(self.account_type_sweep)
    def get_saving_account(self) -> dict:    return self._get_specific_account(self.account_type_savings)

    # ------------------------------------------------
    # Get a list of transactions across all accounts
    # -------------------------------------------------
    def get_all_transactions(self): return self._run_curl_interface(self.api_name_transaction)

    # ------------------------------------------------
    # Get the deposit transactions
    # -------------------------------------------------
    def get_deposit_transactions(self)->list: return self._get_transactions_list(is_deposit_type = True)

    # ------------------------------------------------
    # Get the deposit transactions
    # -------------------------------------------------
    def get_withdrawal_transactions(self)->list: return self._get_transactions_list(is_deposit_type = False)

    # -----------------------------------------------------
    # Get a list of transactions from a specific account
    # ------------------------------------------------------
    def get_specific_transaction(self, tran_id:str): return self._run_curl_interface(self.api_name_transaction + "/" + tran_id)

    # -----------------------------------
    # Get account transactions
    # -----------------------------------
    def get_account_transactions(self, account_type:str) -> dict:
        acct_id = self._get_account_id(account_type)
        if acct_id is None:
            return None
        return self._run_curl_interface(self.api_name_account + "/" + acct_id + "/" + self.api_name_transaction)

    # ------------------------------------------------------------
    # Lock account
    # requires additional permissions in the Treasury Prime API
    # ------------------------------------------------------------
    def lock_account(self, account_type:str):
        acct_id = self._get_account_id(account_type)
        if acct_id is None:
            return None
        data = {}
        data["locked"] = True
        data["reason"] = f"Trying to lock this account: %s" % (acct_id)
        data["additional_context"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return self._run_curl_interface(self.api_name_account + "/" + acct_id, data, self.op_name_patch)

    # -----------------------------------------
    # Transfer money from an account to another
    # ----------------------------------------
    def transfer_money(self, from_account:str, to_account:str, amount:float):
        #amount = str(round(amount, 2))
        amount = f'{amount:.2f}'
        data = {}
        data["amount"] = amount
        data["from_account_id"] = from_account
        data["to_account_id"]   = to_account
        #print(data)
        response = self._run_curl_interface(self.api_name_transfer, data, self.op_name_post)
        if response is None:
            return response
        return response["id"]

    # -----------------------------------
    # Get all book transfers
    # -----------------------------------
    def get_all_transfers(self):
        return self._run_curl_interface(self.api_name_transfer)

    # -----------------------------------
    # Get ma specific transfer
    # -----------------------------------
    def _get_specific_transfer(self, transfer_id) -> dict:
        return self._run_curl_interface(self.api_name_transfer + "/" + transfer_id)

    # ------------------------------------------------
    # Get a list of transactions
    # -------------------------------------------------
    def _get_transactions_list(self, is_deposit_type) -> list:
        numdays = 3 # 30 days back
        from_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-1 * numdays))
        url = self.api_name_transaction + "?from_date=" + from_date
        if is_deposit_type:
            url = url +  "&type=deposit"
        else:
            url = url + "&type=withdrawal"
        trans = self._run_curl_interface(url)
        if trans is None:
            return None
        translist = trans["data"]
        summary_list = []
        for tran in translist:
            tran_rec = {}
            tran_rec["id"] = tran["id"]
            tran_rec["fingerprint"] = tran["fingerprint"]
            tran_rec["desc"] = tran["desc"]
            tran_rec["amount"] = tran["amount"]
            tran_rec["date"] = tran["date"]
            tran_rec["fingerprint"] = tran["fingerprint"]
            if tran["check_id"] is not None:
                tran_rec["tran_id"] = tran["check_id"]
            elif tran["wire_id"] is not None:
                tran_rec["tran_id"] = tran["wire_id"]
            elif tran["book_id"] is not None:
                tran_rec["tran_id"] = tran["book_id"]
            elif tran["billpay_payment_id"] is not None:
                tran_rec["tran_id"] = tran["billpay_payment_id"]
            elif tran["card_id"] is not None:
                tran_rec["tran_id"] = tran["card_id"]
            elif tran["ach_id"] is not None:
                tran_rec["tran_id"] = tran["ach_id"]
            elif tran["trace_id"] is not None:
                tran_rec["tran_id"] = tran["trace_id"]
            else:
                tran_rec["tran_id"] = tran["id"] # Using the ID
                self.glogger.debug("There is no actual ID in the transaction: %s", str(tran))
                continue
            summary_list.append(tran_rec)
        return summary_list

    # -----------------------------------
    # Register a webhook
    # -----------------------------------
    def _register_webhook(self, event_type:str):
        data = {}
        data["event"] = event_type
        data["url"] = self.callback_savvly_web_url
        data["basic_user"] = self.savvly_user_id
        data["basic_secret"] = self.savvly_secret
        return self._run_curl_interface(self.api_name_webhook, data, self.op_name_post)

    # -----------------------------------
    # Get all webhooks
    # -----------------------------------
    def _get_all_webhooks(self):
        return self._run_curl_interface(self.api_name_webhook)

    # -----------------------------------
    # Delete all webhooks
    # -----------------------------------
    def _delete_all_webhooks(self):
        wh_rec = self._get_all_webhooks()
        #print(wh_rec)
        if wh_rec is None:
            self.glogger.info("There is no registered webhook")
            return True
        try:
            wh_list = wh_rec["data"]
        except Exception as err:
            self.glogger.error("There is is no 'Data' in the received dictionary of WEBHOOK list")
            return False
        for wh in wh_list:
            try:
                wh_id = wh["id"]
            except Exception as err:
                self.glogger.error("There is is no 'ID' in the received WEBHOOK record")
                return False
            self.glogger.debug("Deleting webhook %s", wh_id)
            self._run_curl_interface(self.api_name_webhook + "/" + wh_id, None, self.op_name_delete)
        #wh_rec = self._get_all_webhooks()
        #print(wh_rec)

    # -----------------------------------
    # Get account ID
    # -----------------------------------
    def _get_account_id(self, account_type:str):
        account_ids = self.get_account_ids()
        acct_id = None
        for account_rec in account_ids:
            if account_rec["account_type"] == account_type:
                acct_id = account_rec["id"]
                break
        if acct_id is None:
            self.glogger.error("The account_type=%s not found in the account list: %s", account_type, str(account_ids))
            return None
        return acct_id

    # -----------------------------------
    # Get my specific account
    # -----------------------------------
    def _get_specific_account(self, account_type:str) -> dict:
        accounts = self._get_all_accounts([account_type])
        if accounts is None or len(accounts) == 0:
            self.glogger.error("There is no account of type %s", account_type)
            return None
        if len(accounts) > 1:
            self.glogger.error("Too many accounts of type %s. len=%d", account_type, len(accounts))
            return None
        return accounts[0]

    # ---------------------------------------------------
    # Get the list of the accounts
    # A list of account types can be passed to filter
    # ---------------------------------------------------
    def _get_all_accounts(self, account_types:list=None) -> list:
        accounts_dict = self._run_curl_interface(self.api_name_account)
        try:
            accounts_list = accounts_dict["data"]
        except Exception as err:
            self.glogger.error("accounts_dict is invalid - expected to find a list at key: data")
            return None
        required_account_list = []
        for account in accounts_list:
            try:
                account_type = account["account_type"]
            except Exception as err:
                self.glogger.error("accounts_list is invalid - expected to find account_type")
                return None
            if account_types is not None and account_type not in account_types:
                continue #Ignore this account
            try:
                id = account["id"]
            except Exception as err:
                self.glogger.error("account is invalid - expected to find id")
                return None
            # print(id)
            api_name = self.api_name_account
            account_details = self._get_account_details(id)
            if not isinstance(account_details, dict):
                self.glogger.error("Unexpected type of data received from API (expected dict).")
                return None
            account_details["id"] = id
            # print(account_details)
            required_account_list.append(account_details)
        # print(required_account_list)
        return (required_account_list)

    # -----------------------------------
    # Get account list
    # -----------------------------------
    def _get_account_details(self, account_id): return self._run_curl_interface(self.api_name_account + "/" + account_id)

    # -----------------------------------
    # Escape the special characters
    # -----------------------------------
    def _escape_convert_to_string(self, data : dict) -> str:
        if not data:
            return None
        #print("ORG:")
        #print(data)
        data = json.dumps(data)
        #print("STRING:")
        #print(data)
        #escaped_data = data.replace('"', '\"')
        #escaped_data = escaped_data.replace('\'', '"')
        #print("ESCAPED:")
        #print(escaped_data)
        #print("Type of escaped" + str(type(escaped_data)))
        #return escaped_data
        #data = json.dumps(data).encode('utf-8')
        #data = data.replace('"', '\\"')
        #print("ESCAPED:" + str(type(data)))
        #print(data)
        return data

    # -----------------------------------
    # Run a CURL interface
    # -----------------------------------
    def _run_curl_interface(self, api : str, data : dict = None, operation : str = "get") -> dict:
        if api:
            url = self.url + "/" + api
        else:
            url = self.url
        #headers = {"Content-type": "application/json", "Accept": "application/json"}
        headers = {"Content-type": "application/json"}
        data = self._escape_convert_to_string(data)

        auth = HTTPBasicAuth(self.key, self.secret)

        try:
            op_list={self.op_name_post: requests.post, self.op_name_get: requests.get,
                     self.op_name_patch:requests.patch, self.op_name_delete: requests.delete}
            req_func = op_list[operation]
        except Exception as err:
            self.glogger.error("Invalid operation: %s. URL=%s op=%s data=%s. err=%s", url, operation, data, err)
            return None

        response = req_func(url, auth=auth, headers=headers, data=data)
        if  response is None:
            self.glogger.error("Requests returned a an invalid response (None). URL=%s op=%s data=%s", url, operation, data)
            return None
        status = response.status_code
        if status > 210:
           self.glogger.error("Failed to run a request. URL=%s op=%s data=%s status=%d", url, operation, data, status)
           return None
        if status == 204:  # No content
            return ""
        response_dict = json.loads(response.text)
        self.glogger.debug("Status=%d URL:%s Response:%s", status, url, response_dict)
        return response_dict

