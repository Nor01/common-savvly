#import os
#import time
from common.util.logging_helper import get_logger, logger_get_old_log_files, logger_get_log_filename
from common.models.azure_file_storage import *
from common.controllers.dbhandles import *
from common.controllers.contract import *
from common.controllers.contract_storage import *

#---------------------------------------------
# Sync the contract files on the storage
#---------------------------------------------
class SyncStorageContract:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("synccontractstorage")
        self.azfileclient = AzureFileStorage.get_instance()
        self.dbhandles = Dbhandles.get_instance()  # Get the instance of the dbhandles

    # ----------------------------------------------------------------------
    # Sync the files
    # ----------------------------------------------------------------------
    def sync(self):
        try:
            files_list = self.azfileclient.list_contracts()
            self.glogger.debug("There are %d contracts on Azure Storage", len(files_list))
            if files_list is None or len(files_list) == 0:
                return
            self.glogger.debug("Contract List on Azure: %s", files_list)
            userinfo_list = self.dbhandles.get_usertables().get_all_contracts()
            self.glogger.debug("There are %d contracts in the DB", len(userinfo_list))
            self.glogger.debug("Contract List in the DB: %s", userinfo_list)
            for userinfo in userinfo_list:
                try:
                    self.glogger.debug("User Info in the DB: %s", userinfo)
                    contract_id = userinfo["contract_id"]
                    if contract_id is None:
                        self.glogger.error("The retrevied record from the DB has no contact ID: %s", userinfo)
                        continue
                    if self._check_existense(contract_id, files_list):
                        continue
                    self.glogger.info("The contract (%s) does not exist on Azure Storage", contract_id)
                    docusign_helper = DocuSignContractHelper(contract_id)
                    contract_url = docusign_helper.get_contract_url()
                    self.glogger.info("Uploading the contract to Azure ContractID=%s URL=%s", contract_id, contract_url)
                    ContractStorage().store(contract_url, contract_id, userinfo['advisor_id'], userinfo['email'], userinfo['idx'])
                except Exception as err:
                    self.glogger.error("Exception while syncing the contract of this user:%s (err=%s)", userinfo, err)
                    continue
        except Exception as err:
            self.glogger.error("Exception while syncing the contract files on Azure with signed contact. err=%s")
            return

    # ----------------------------------------------------------------------
    # Check if the contract exist in the files list
    # ----------------------------------------------------------------------
    def _check_existense(self, contract_id, files_list):
        if contract_id in files_list:
            self.glogger.debug("The contract (%s) exists on the Azure Storage", contract_id)
            return True
        return False