import os
from common.util.logging_helper import get_logger
from common.models.azure_file_storage import *
from common.controllers.dbhandles import *

#---------------------------------------------
# Store contracts
#---------------------------------------------
class ContractStorage:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("contractstore")
        self.azfileclient = AzureFileStorage.get_instance()
        self.dbhandles = Dbhandles.get_instance()  # Get the instance of the dbhandles

    # ----------------------------------------------------------------------
    # Store a contract
    # ----------------------------------------------------------------------
    def store(self, contract_url: str, contract_id:str, advisor: str, client:str, clientid: str):
        self.glogger.info("Storing contract (id=%s) between %s and %s (id=%s)", contract_id, advisor, client, clientid)
        file_location = self.azfileclient.download_contract_and_store(contract_url, contract_id)
        if file_location is None:
            self.glogger.error("Failed to store the contract (id=%s, url=%s) on the storage",contract_id, contract_url)
            return False
        self.glogger.info("Saving the contract info in the database id=%s url=%s location=%s", contract_id, contract_url, file_location)
        description = f"Contract between {advisor} and {client}"
        return self.dbhandles.get_filetables().add_contract(contract_id, description, clientid, file_location)

    # ----------------------------------------------------------------------
    # Upload a contract and store in the database
    # ----------------------------------------------------------------------
    def upload(self):
        fname_list = FsFiles().upload_files() # Returns the list of the files uplaoded to the Upload Directory
        if fname_list is None:
            self.glogger.error("Failed uo upload files from local host to the server")
            return False
        for fname in fname_list:
            local_file_path =  os.path.join(utils_get_upload_folder(), fname)
            self.glogger.info("Uploading the file %s to Azure", local_file_path)
            uploaded_to_az = self.azfileclient.upload_contract(local_file_path)
            if uploaded_to_az is None:
                self.glogger.error("Failed to upload %s from the server to Azure", local_file_path)
                continue
            self.dbhandles.get_filetables().add_contract(fname, "default description", "default client", "From Host")
        return True
