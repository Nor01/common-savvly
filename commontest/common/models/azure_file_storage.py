import os
import requests
from azure.storage.fileshare import ShareServiceClient, ShareClient, ShareDirectoryClient, ShareFileClient
from common.util.logging_helper import get_logger
from common.util.utils_file_rw import *

#---------------------------------------------
# File System on Azure
#---------------------------------------------
class AzureFileStorage:
    folder_contracts = "Contracts"
    folder_logs = "Logs"
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if AzureFileStorage.__instance is None:
            AzureFileStorage()
        return AzureFileStorage.__instance

    # ----------------------------------------------------------------------
    # Constructor
    # Source: https://docs.microsoft.com/en-us/azure/storage/files/storage-python-how-to-use-file-storage?tabs=python
    # ----------------------------------------------------------------------
    def __init__(self, share_name=None):
        if AzureFileStorage.__instance != None:
            raise Exception("This class (AzureFileStorage) is a singleton!")
            return
        AzureFileStorage.__instance = self
        self.glogger = get_logger("azfile")
        self.connection_string="DefaultEndpointsProtocol=https;AccountName=savvlystorage;AccountKey=r+t6UbtW/oeXOBpiuIsk7VDM1F50+vI8MEcAEgatxXSrJYVzcpHedvoDmLq8mXUzwbBNdy3orMUZ+AStc8sQpA==;EndpointSuffix=core.windows.net"
        if share_name is None:
            self.share_name = "sharedfiles" # All characters must be lower case
        else:
            self.share_name = share_name.lower()
        self.create_share()
        self.create_contract_directory()
        self.create_logs_directory()

    # ----------------------------------------------------------------------
    # Create a share
    # ----------------------------------------------------------------------
    def create_share(self):
        try:
            # Create a ShareClient from a connection string
            share_client = ShareClient.from_connection_string(self.connection_string, self.share_name)
            self.glogger.info("Creating share: %s", self.share_name)
            share_client.create_share()
            return True
        except Exception as err:
            self.glogger.error("Exception to create a share (%s). err=%s", self.share_name, err)
            return False

    # ----------------------------------------------------------------------
    # Delete a share
    # ----------------------------------------------------------------------
    def delete_share(self):
        try:
            # Create a ShareClient from a connection string
            share_client = ShareClient.from_connection_string(self.connection_string, self.share_name)
            self.glogger.info("Deleting share: %s", self.share_name)
            # Delete the share and snapshots
            share_client.delete_share(delete_snapshots=True)
            return True
        except Exception as err:
            self.glogger.error("Exception to delete a share (%s). err=%s", self.share_name, err)
            return False

    # ----------------------------------------------------------------------
    # Create a folder
    # ----------------------------------------------------------------------
    def create_directory(self, dir_name):
        try:
            # Create a ShareDirectoryClient from a connection string
            dir_client = ShareDirectoryClient.from_connection_string(self.connection_string, self.share_name, dir_name)
            self.glogger.info("Creating directory: %s/%s", self.share_name, dir_name)
            dir_client.create_directory()
            return True
        except Exception as err:
            self.glogger.error("Exception to create a directory (%s). err=%s", dir_name, err)
            return False

    # ----------------------------------------------------------------------
    # Create a folder
    # ----------------------------------------------------------------------
    def list_files_and_dirs(self, dir_name):
        file_list = []
        try:
            # Create a ShareClient from a connection string
            share_client = ShareClient.from_connection_string(self.connection_string, self.share_name)
            for item in list(share_client.list_directories_and_files(dir_name)):
                name = item["name"]
                if item["is_directory"]:
                    self.glogger.info("Directory: %s", name)
                else:
                    self.glogger.info("File: %s/%s", dir_name, name)
                    file_list.append(name)
            return file_list
        except Exception as err:
            self.glogger.error("Exception to list files and dirs (%s). err=%s", dir_name, err)
            return None

    # ----------------------------------------------------------------------
    # Upload a file
    # Retuns the path the files uploaded to
    # ----------------------------------------------------------------------
    def upload_file(self, local_file_path, dest_file_path):
        try:
            source_file = open(local_file_path, "rb")
            data = source_file.read()
            # Create a ShareFileClient from a connection string
            file_client = ShareFileClient.from_connection_string(self.connection_string, self.share_name, dest_file_path)
            self.glogger.info("Uploading to: %s/%s", self.share_name, dest_file_path)
            file_client.upload_file(data)
            return dest_file_path
        except Exception as err:
            self.glogger.error("Exception to upload the file %s to %s. err=%s", local_file_path, dest_file_path, err)
            return None

    # ----------------------------------------------------------------------
    # Upload a file to a specific directory
    # Retuns the path the file uploaded to
    # ----------------------------------------------------------------------
    def upload_file_to_dir(self, local_file_path, dir_name):
        try:
            basename = os.path.basename(local_file_path)
            dest_file_path = os.path.join(dir_name, basename)
            return self.upload_file(local_file_path, dest_file_path)
        except Exception as err:
            self.glogger.error("Exception to split file name from:%s, err=%s", local_file_path, err)
            return None

    # ----------------------------------------------------------------------
    # Download a file
    # Retuns the full path of the downloaded file
    # ----------------------------------------------------------------------
    def download_file(self, dir_name, file_name):
        try:
            # Build the remote path
            source_file_path = dir_name + "/" + file_name

            # Create a ShareFileClient from a connection string
            file_client = ShareFileClient.from_connection_string(self.connection_string, self.share_name, source_file_path)
            dest_file_name = file_name
            self.glogger.info("Downloading to: %s", dest_file_name)
            # Open a file for writing bytes on the local system
            with open(dest_file_name, "wb") as data:
                # Download the file from Azure into a stream
                stream = file_client.download_file()
                # Write the stream to the local file
                data.write(stream.readall())
            return dest_file_name
        except Exception as err:
            self.glogger.error("Exception to download file: %s/%s, err=%s", dir_name, file_name, err)
            return None

    # ----------------------------------------------------------------------
    # Download a file from a URL and store on Azure
    # Retuns the path the file uploaded to
    # ----------------------------------------------------------------------
    def download_file_from_url_and_store(self, url, file_name, dir_name):
        pathname = utils_download_file_by_url(url, file_name)
        if pathname is None:
            self.glogger.error("Failed to download the file from %s and store in %s", url, file_name)
            return None
        return self.upload_file_to_dir(pathname, dir_name)

    # ----------------------------------------------------------------------
    # Delete a file
    # ----------------------------------------------------------------------
    def delete_file(self, file_path):
        try:
            # Create a ShareFileClient from a connection string
            file_client = ShareFileClient.from_connection_string(self.connection_string, self.share_name, file_path)
            self.glogger.info("Deleting file: %s/%s", self.share_name, file_path)
            file_client.delete_file()  # Delete the file
            return True
        except Exception as err:
            self.glogger.error("Exception to delete file: %s, err=%s", file_path, err)
            return False

    # ----------------------------------------------------------------------
    # Delete a file from a dir
    # ----------------------------------------------------------------------
    def delete_file_from_dir(self, dir_name, file_name):
        file_path = dir_name + "/" + file_name
        return self.delete_file(file_path)

    # ----------------------------------------------------------------------
    # Create Contracts Directory
    # ----------------------------------------------------------------------
    def create_contract_directory(self): return self.create_directory(self.folder_contracts)

    # ----------------------------------------------------------------------
    # Create Contracts Directory
    # Retuns the path the file uploaded to
    # ----------------------------------------------------------------------
    def list_contracts(self): return self.list_files_and_dirs(self.folder_contracts)

    # ----------------------------------------------------------------------
    # Upload a contract
    # Retuns the path the file uploaded to
    # ----------------------------------------------------------------------
    def upload_contract(self, local_file_path): return self.upload_file_to_dir(local_file_path, self.folder_contracts)

    # ----------------------------------------------------------------------
    # Download a contract
    # Retuns the full path of the downloaded file
    # ----------------------------------------------------------------------
    def download_contract(self, file_name): return self.download_file(self.folder_contracts, file_name)

    # ----------------------------------------------------------------------
    # Delete a contract
    # ----------------------------------------------------------------------
    def delete_contract(self, file_name): return self.delete_file_from_dir(self.folder_contracts, file_name)

    # ----------------------------------------------------------------------
    # Download a contract from URL and store on Azure
    # Retuns the path the file uploaded to
    # ----------------------------------------------------------------------
    def download_contract_and_store(self, contract_url, contract_id):
        return self.download_file_from_url_and_store(contract_url, contract_id, self.folder_contracts)

    # ----------------------------------------------------------------------
    # Create Logs Directory
    # ----------------------------------------------------------------------
    def create_logs_directory(self): return self.create_directory(self.folder_logs)

    # ----------------------------------------------------------------------
    # Upload a log file
    # Returns the path the file uploaded to
    # ----------------------------------------------------------------------
    def upload_log_file(self, local_file_path): return self.upload_file_to_dir(local_file_path, self.folder_logs)
