#import os
#import glob
#import werkzeug
#import time
#from pathlib import Path
#from flask import send_from_directory
#from common.util.utility_functions import *
##from models.image import *
#from common.util.logging_helper import get_logger, logger_get_log_filename
#
## -----------------------------------
## Create an instrance of the logger
## -----------------------------------
#glogger = get_logger("fileop")

# ---------------------------------------------------------------
# Upload file to the server
# ---------------------------------------------------------------
#def fileop_upload_files_2fs(files_ids : list) -> list:
#    image_num = 1
#    fname_list=[]
#    folder = utils_get_upload_folder()
#    for file_id in files_ids:
#        glogger.info("Saving file %d / %d", image_num, len(files_ids))
#        uploadfile = files_ids[file_id]
#        filename = ""
#        try:
#            filename = werkzeug.utils.secure_filename(uploadfile.filename)
#            glogger.info("Image Filename : %s", uploadfile.filename)
#            timestr = time.strftime("%Y%m%d-%H%M%S")
#            filename = timestr + '_' + filename
#            file_path = os.path.join(folder, filename)
#            uploadfile.save(file_path)
#            image_num = image_num + 1
#            fname_list.append(file_path)
#            glogger.info("List of files: %s", fname_list)
#        except Exception as err:
#            glogger.error("Failed to upload file %s (%d). err=%s", filename, image_num, err)
#            return None
#    return fname_list

# -------------------------------------------------------
# List the files in the home directory
# Example from here: https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html
# -------------------------------------------------------
#def fileop_list_fs_files() -> list:
#    files = []
#    folder = utils_get_upload_folder()
#    for filename in os.listdir(folder):
#        path = os.path.join(folder, filename)
#        if os.path.isfile(path):
#            files.append(filename)
#    return files

# -------------------------------------------------------
# Delete files in the home directory
# -------------------------------------------------------
#def fileop_delete_fs_files(file_ext):
#    folder = utils_get_upload_folder()
#    files_wildcard = os.path.join(folder, "*." + file_ext)
#    file_list = glob.glob(files_wildcard)
#    for file_path in file_list:
#        try:
#            glogger.info("Deleting file : %s", file_path)
#            os.remove(file_path)
#        except:
#            glogger.error("Error while deleting file : %s", file_path)
#    return file_list

# -------------------------------------------------------
# Download a file
# -------------------------------------------------------
#def fileop_download_fs_file(file_name):
#    folder = utils_get_download_folder()
#    return _fileop_download_file(folder, file_name)

# -------------------------------------------------------
# Download Log Files
# -------------------------------------------------------
#def fileop_download_logfile() -> str:
#    file_path = logger_get_log_filename()
#    folder = str(Path.home())
#    try:
#        fname = os.path.basename(file_path)
#        glogger.info("Downloading file : %s from folder %s", fname, folder)
#        result = _fileop_download_file(folder, fname)
#    except Exception as err:
#        glogger.error("Error while Downloading log file : %s from folder %s, err=%s", fname, folder, err)
#        return None
#    return result

# -------------------------------------------------------
# Download User Photo
# -------------------------------------------------------
#def fileop_download_user_image(puserobj, userid) -> str:
#    if puserobj is None:
#        glogger.error("The user object is None - cannot download user image: %s", userid)
#        return None
#    glogger.info("Getting the photo of the user %s", userid)
#    fname = _fileop_store_user_image_in_file(puserobj, userid)
#    if not fname:
#        return None
#    result = fileop_download_file(fname)
#    glogger.info("The photo of the user %s downloaded by file %s", userid, result)
#    return result

# -------------------------------------------------------
# Download a file
# -------------------------------------------------------
#def _fileop_download_file(folder, file_name):
#    file_path = os.path.join(folder, file_name)
#    if not os.path.isfile(file_path):
#        glogger.info("File not found: %s. Cannot download", file_path)
#        return None
#    file_name = os.path.basename(file_path)
#    glogger.info("Downloading file: %s from folder:%s", file_name, folder)
#    try:
#        result = send_from_directory(folder, file_name, as_attachment=True)
#    except Exception as err:
#        glogger.error("Exception from send_from_directory while downloading %s from folder %s. err=%s", file_name, folder, err)
#        return None
#    glogger.info("Download file result: %s", result)
#    return result

# -------------------------------------------------------
# Get User Photo as a file (return file name)
# -------------------------------------------------------
#def _fileop_store_user_image_in_file(puserobj, userid:str) -> str:
#    glogger.info("Going to get the user image from the db: %s", userid)
#    try:
#        image = image_get(puserobj, userid)
#        if not image:
#            glogger.error("Failed to get user image: %s", userid)
#            return None
#        folder = utils_get_temp_folder()
#        file_name = os.path.join(folder, userid + ".img")
#        file = open(file_name, "wb")
#        if not file:
#            glogger.error("Failed to create a file name to store the image in: %s", file_name)
#            return None
#        file.write(image)
#        file.close()
#    except Exception as err:
#        glogger.info("Storing image failed. err=%s", err)
#        return None
#    glogger.info("The user image stored in %s", file_name)
#    return file_name


# -------------------------------------------------------
# Set Image file to the user
# -------------------------------------------------------
#def _fileop_set_user_image(puserobj, userid, filename) -> str:
#    glogger.info("Setting photo for the user %s: %s", userid, filename)
#    bytes_read = None
#    try:
#        with open(filename, "rb") as file:
#            bytes_read = file.read()   # No need to close - It is closed automatically
#        if not bytes_read:
#            glogger.error("Failed to read the file %s that contains the user photo", filename)
#            return None
#        if not image_store(puserobj, userid, bytes_read):
#            glogger.error("Failed to store the photo of the user: %s via file %s", userid, filename)
#            return None
#        glogger.info("The photo of the user %s uploaded via the file %s (size=%d)", userid, filename, len(bytes_read))
#        return filename
#    except Exception as err:
#        glogger.error("Failed to read the file %s of user=%s. err=%s", filename, userid, err)
#        return None

# -------------------------------------------------------
# Upload User Photo
# -------------------------------------------------------
#def fileop_upload_files_2db(puserobj, userid : str, file_list : list) -> str:
#    if puserobj is None:
#        glogger.error("The user object is None - cannot upload user image: %s", userid)
#        return None
#    if len(file_list) < 1:
#        glogger.error("No file was passed to upload")
#        return None
#    if len(file_list) != 1:
#        glogger.error("Too many files passed for uploading user photo (%d)", len(file_list))
#    filename = file_list[0]
#    return _fileop_set_user_image(puserobj, userid, filename)

# -------------------------------------------------------
# Set default image to the user
# -------------------------------------------------------
#def fileop_set_default_image(puserobj, userid):
#    if puserobj is None:
#        glogger.error("The user object is None - cannot set default image: %s", userid)
#        return None
#    filename = utils_get_default_user_image()
#    if not filename:
#        glogger.info("The default image file not found: %s.", filename)
#        return None
#    return _fileop_set_user_image(puserobj, userid, filename)