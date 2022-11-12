import os
from common.util.logging_helper import get_logger, logger_get_old_log_files
from common.models.azure_file_storage import *
from  common.models.fs_files import *

#---------------------------------------------
# Store Log Files
#---------------------------------------------
class LogFilesStorage:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("logfilestore")
        self.azfileclient = AzureFileStorage.get_instance()

    # ----------------------------------------------------------------------
    # Store the log files from our server to the Azure Storage
    # ----------------------------------------------------------------------
    def upload(self):
        try:
            files_list = logger_get_old_log_files()
            if files_list is None or len(files_list) == 0:
                self.glogger.info("No old log file found on the server")
                return
            self.glogger.info("%d old log files found on the server: %s", len(files_list), files_list)
            for fname in  files_list:
                self.glogger.info("Uploading the old log file to Azure: %s", fname)
                file_location = self.azfileclient.upload_log_file(fname)
                if file_location is None:
                    self.glogger.error("Failed to upload old log file %s to the storage", fname)
                    continue
            for fname in  files_list:
                self.glogger.info("The old log file %s uploaded to Azure: %s", fname, file_location)
                FsFiles().delete_file(fname)
        except Exception as err:
            self.glogger.info("Exception to upload the old log files to the storage: %s",err)
