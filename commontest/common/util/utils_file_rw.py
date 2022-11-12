import requests
import os
from common.util.logging_helper import get_logger
from common.util.utility_functions import *

# -------------------------------------------------------
# Read a file
# -------------------------------------------------------
def utils_read_file(file_name : str) -> bytearray:
    glogger = get_logger("utils")
    try:
        with open(file_name, "rb") as file:
            bytes_read = file.read()  # No need to close - It is closed automatically
        if not bytes_read:
            glogger.error("Failed to read the file %s", file_name)
            return None
        return bytes_read
    except Exception as err:
        glogger.info("Failed to read file %s. err=%s", file_name, err)
    return None

# -------------------------------------------------------
# Write a bytearray to a file
# -------------------------------------------------------
def utils_write_file(data: bytearray, file_name : str) -> str:
    glogger = get_logger("utils")
    try:
        file = open(file_name, "wb")
        if not file:
            glogger.error("Failed to create a file name to store the image in: %s", file_name)
            return None
        file.write(data)
        file.close()
    except Exception as err:
        glogger.info("Storing data in file %s failed. err=%s", file_name, err)
        return None
    return file_name

# ---------------------------------------------------------------
# Download a file from a URL
# ---------------------------------------------------------------
def utils_download_file_by_url(url:str, dest_fname : str) -> str:
    glogger = get_logger("utils")
    try:
        response = requests.get(url)
    except Exception as err:
        glogger.error("Failed to download file from url=%s err=%s", url, err)
        return None
    try:
        folder = utils_get_download_folder()
        file_path = os.path.join(folder, dest_fname)
        utils_write_file(response.content, file_path)
    except Exception as err:
        glogger.error("Failed to save the downloaded file from url=%s err=%s", url, err)
        return None
    return file_path