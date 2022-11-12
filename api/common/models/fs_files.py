import os
import glob
import werkzeug
import time
import requests
from pathlib import Path
from flask import request
from flask import send_from_directory
from common.util.utility_functions import *
from common.util.utils_file_rw import *
from common.util.logging_helper import get_logger, logger_get_log_filename

# -----------------------------------------------------------------------------------------------------------------------
# File System files
# -----------------------------------------------------------------------------------------------------------------------
class FsFiles():
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("FsFiles")

    # -------------------------------------------------------
    # Download Log Files
    # Returns Streem
    # -------------------------------------------------------
    def download_logfile(self) -> str:
        file_path = logger_get_log_filename()
        folder = str(Path.home())
        try:
            fname = os.path.basename(file_path)
            self.glogger.debug("Downloading file : %s from folder %s", fname, folder)
            result = self.download_file(folder, fname)
        except Exception as err:
            glogger.error("Error while Downloading log file : %s from folder %s, err=%s", fname, folder, err)
            return None
        return result

    # -------------------------------------------------------
    # List the files in the upload directory
    # -------------------------------------------------------
    def list_uploaded_files(self) -> list:
        folder = utils_get_upload_folder()
        return self._list_files(folder)

    # -------------------------------------------------------
    # List the files in the download directory
    # -------------------------------------------------------
    def list_downloaded_files(self) -> list:
        folder = utils_get_download_folder()
        return self._list_files(folder)

    # -------------------------------------------------------
    # Delete files in the upload directory
    # -------------------------------------------------------
    def delete_uploaded_files(self, file_ext):
        folder = utils_get_upload_folder()
        return self._delete_files(folder, file_ext)

    # -------------------------------------------------------
    # Delete file in the Upload directory
    # -------------------------------------------------------
    def delete_uploaded_file(self, file_name):
        folder = utils_get_upload_folder()
        full_file_name = os.path.join(folder, file_name)
        return self.delete_file(full_file_name)

    # -------------------------------------------------------
    # Delete files in the download directory
    # -------------------------------------------------------
    def delete_downloaded_files(self, file_ext):
        folder = utils_get_download_folder()
        return self._delete_files(folder, file_ext)

    # -------------------------------------------------------
    # Delete file in the Download directory
    # -------------------------------------------------------
    def delete_downloded_file(self, file_name):
        folder = utils_get_download_folder()
        full_file_name = os.path.join(folder, file_name)
        return self.delete_file(full_file_name)

    # -------------------------------------------------------
    # Download a file
    # -------------------------------------------------------
    def download_file(self, folder, file_name):
        file_path = os.path.join(folder, file_name)
        if not os.path.isfile(file_path):
            self.glogger.info("File not found: %s. Cannot download", file_path)
            return None
        file_name = os.path.basename(file_path)
        self.glogger.info("Downloading file: %s from folder:%s", file_name, folder)
        try:
            result = send_from_directory(folder, file_name, as_attachment=True)
        except Exception as err:
            self.glogger.error("Exception while downloading %s from folder %s. err=%s", file_name, folder, err)
            return None
        self.glogger.debug("Download file result: %s", result)
        return result

    # -------------------------------------------------------
    # Download a file from the upload-folder
    # -------------------------------------------------------
    def download_file_from_upload_folder(self, file_name): self.download_file(utils_get_upload_folder(), file_name)

    # -------------------------------------------------------
    # Download a file from the download-folder
    # -------------------------------------------------------
    def download_file_from_download_folder(self, file_name): self.download_file(utils_get_download_folder(), file_name)

    # ---------------------------------------------------------------
    # Download a file
    # ---------------------------------------------------------------
    def download_url_file(self, url:str, dest_fname : str) -> str:
        try:
            response = requests.get(url)
        except Exception as err:
            self.glogger.error("Failed to download file from url=%s err=%s", url, err)
            return None
        try:
            folder = utils_get_download_folder()
            file_path = os.path.join(folder, dest_fname)
            utils_write_file(response.content, file_path)
            #open(file_path, "wb").write(response.content)
        except Exception as err:
            self.glogger.error("Failed to save the downloaded file from url=%s err=%s", url, err)
            return None
        return file_path

    # ---------------------------------------------------------------
    # Upload files to the server (return file names only)
    # ---------------------------------------------------------------
    def upload_files(self, add_time_prefix : bool = False):
        if not request.files:
            self.glogger.error("The files list is non in the request. Invalid files list.")
            return None
        files_ids = list(request.files)
        self.glogger.info("Number of uploading files : %d", len(files_ids))
        return self._upload_files(files_ids, add_time_prefix)

    # -------------------------------------------------------
    # List the files in the home directory
    # Example from here: https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html
    # -------------------------------------------------------
    def _list_files(self, folder) -> list:
        files = []
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if os.path.isfile(path):
                files.append(filename)
        return files

    # -------------------------------------------------------
    # Delete file
    # -------------------------------------------------------
    def delete_file(self, full_file_name):
        try:
            self.glogger.info("Deleting file : %s", full_file_name)
            os.remove(full_file_name)
        except Exception as err:
            self.glogger.error("Error while deleting file : %s err=%s", full_file_name, err)
            return None
        return full_file_name

    # -------------------------------------------------------
    # Delete files in the specified directory
    # -------------------------------------------------------
    def _delete_files(self, folder, file_ext):
        files_wildcard = os.path.join(folder, "*." + file_ext)
        file_list = glob.glob(files_wildcard)
        for file_path in file_list:
            try:
                self.glogger.info("Deleting file : %s", file_path)
                os.remove(file_path)
            except Exception as err:
                self.glogger.error("Error while deleting file : %s err=%s", file_path, err)
                continue
        return file_list

    # ---------------------------------------------------------------
    # Upload files to the server
    # The list is is objects of type: FileStorage
    # ---------------------------------------------------------------
    def _upload_files(self, uploadfile_list: list, add_time_prefix : bool) -> list:
        fname_list=[]
        for file_id in uploadfile_list:
            uploadfile = _uploadfile_list[file_id]
            filename = self._upload_file(uploadfile, add_time_prefix)
            if filename is None:
                continue
            fname_list.append(file_path)
        return fname_list

    # ---------------------------------------------------------------
    # Upload a file to the server
    # the uploadfile is of type : FileStorage
    # ---------------------------------------------------------------
    def _upload_file(self, uploadfile, add_time_prefix : bool):
        folder = utils_get_upload_folder()
        try:
            filename = werkzeug.utils.secure_filename(uploadfile.filename)
            self.glogger.info("Uloading file=%s to folder %s / %d", uploadfile.filename, folder)
            if add_time_prefix:
                timestr = time.strftime("%Y%m%d-%H%M%S")
                filename = timestr + '_' + filename
            file_path = os.path.join(folder, filename)
            uploadfile.save(file_path)
        except Exception as err:
            self.glogger.error("Failed to upload file %s. err=%s", uploadfile.filename, err)
            return None
        self.glogger.info("Uploaded: %s", filename)
        return filename


