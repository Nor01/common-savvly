import os
import time
from common.util.logging_helper import get_logger, logger_get_old_log_files, logger_get_log_filename
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
    def upload_old_log_files(self):
        try:
            files_list = logger_get_old_log_files()
            if files_list is None or len(files_list) == 0:
                self.glogger.debug("No old log file found on the server")
                return
            self.glogger.debug("%d old log files found on the server: %s", len(files_list), files_list)
            for fname in  files_list:
                self.glogger.info("Uploading the old log file to Azure: %s", fname)
                file_location = self.azfileclient.upload_log_file(fname, add_time_suffix=False)
                if file_location is None:
                    self.glogger.error("Failed to upload old log file %s to the storage", fname)
                    continue
            for fname in  files_list:
                self.glogger.info("The old log file %s uploaded to Azure: %s", fname, file_location)
                FsFiles().delete_file(fname)
        except Exception as err:
            self.glogger.info("Exception to upload the old log files to the storage: %s",err)

    # ----------------------------------------------------------------------
    # Store the current log file from our server to the Azure Storage
    # This function is used before the server upgrade to save the logs
    # on nthe storage
    # ----------------------------------------------------------------------
    def upload_current_log_file(self):
        try:
            log_fname = logger_get_log_filename()
            self.glogger.debug("Uploading the current log file to Azure: %s", log_fname)
            file_location = self.azfileclient.upload_log_file(log_fname, add_time_suffix=True)
            if file_location is None:
                self.glogger.error("Failed to upload log file %s to the storage", log_fname)
                return False
            return True
        except Exception as err:
            self.glogger.info("Exception to upload the current log file to the storage: %s",err)
            return False
