import base64
import copy
import json
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------
# Create an instance of the logger (This must be before our imports )
# ----------------------------------------------------------------------
from common.util.logging_helper import get_logger

# ---------------------------------
# Global Variable - Logger
# ---------------------------------
glogger = get_logger("api")


# ---------------------------------
# Return Version
# ---------------------------------
#def utils_get_version():
#    version = "0.18"
#    if is_dev_env():
#        version = version + "D"
#    else:
#        version = version + "P"
#    return version


# ---------------------------------------------------
# Are we in PROD environment or Dev environment
# ---------------------------------------------------
def utils_is_dev_env():
    runenv = "dev"
    try:
        runenv = os.environ['API_ENVIRONMENT']
    except KeyError:
        glogger.error("Environment variable (API_ENVIRONMENT) required - assuming it is dev otherwise")
        os.environ['API_ENVIRONMENT'] = runenv
        return True
    if runenv == "dev":
        return True  # Dev Environment
    return False  # Product Environment


# ---------------------------------
# Get a random number
# ---------------------------------
def get_randomizer():
    ###    timestamp = int(time.time()* random.random())
    timestamp = int(time.time() * 10000)
    return str(timestamp)


# ---------------------------------
# Convert type safely
# ---------------------------------
def utils_convert_to_type(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

# ------------------------------------------------------
# Get Running Directory
# ------------------------------------------------------
def utils_get_running_dir():
    main_script_name = os.path.abspath(sys.argv[0])
    path_info = os.path.split(main_script_name)
    main_dir = path_info[0] + os.sep
    return main_dir

# ---------------------------------
# Get file path
# ---------------------------------
def find_file_path(name, path="/../../.."):
    for root, dirs, files in os.walk(path):
        # print("{} {} {}".format(root, dirs, files))
        if name in files:
            return os.path.join(root, name)
    return None

# ----------------------------------------
# Get temporary folder
# ----------------------------------------
def utils_get_temp_folder():
    home = str(Path.home())
    dir_path = os.path.join(home, 'temp')  # Changed it to the same name as upload
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

# ----------------------------------------
# Get folder for upload files
# ----------------------------------------
def utils_get_upload_folder():
    return utils_get_temp_folder()  # Changed it to the same name as temp

# ----------------------------------------
# Get folder for download files
# ----------------------------------------
def utils_get_download_folder():
    return utils_get_temp_folder()  # Changed it to the same name as temp

# ------------------------------------------------------
# Convert list of jsons to list of strings
# ------------------------------------------------------
def utils_jsonlist_to_strlist(jsonlist: list) -> list:
    strlist = list()
    for jsn in jsonlist:
        st = json.dumps(jsn)
        strlist.append(st)
    return strlist


# ------------------------------------------------------
# If a value exists in the list
# ------------------------------------------------------
def utils_is_value_in_list(list, value):
    # traverse in the 1st list
    for x in list:
        if x == value:
            return True
    return False


# ------------------------------------------------------
# if two lists have at-least one element common
# ------------------------------------------------------
def utils_common_data_in_two_lists(list1, list2):
    # traverse in the 1st list
    for x in list1:
        # traverse in the 2nd list
        for y in list2:
            # if one common
            if x == y:
                return True
    return False


# ------------------------------------------------------
# Get the full path of the default image
# ------------------------------------------------------
def utils_get_default_user_image():
    folder = os.getcwd()
    file_name = os.path.join(folder, "default_user_photo.png")
    if not os.path.isfile(file_name):
        return None
    return file_name


# ------------------------------------------------------
# Print attrobutes and values of an object
# ------------------------------------------------------
def utils_get_object_values(obj):
    str = vars(obj)
    print(str)
    return str


# -------------------------------------------------------------------------------
# Serialize the storing data
# -------------------------------------------------------------------------------
def utils_serialize_data(user_data):
    glogger.info("Serialize: UserData=%s", user_data)
    data_str = user_data.encode('ascii')
    data = base64.b64encode(data_str)
    db_data = data.decode('UTF-8')
    glogger.info("Serialize: UserData=%s, DBData=%s", user_data, db_data)
    return db_data


# -------------------------------------------------------------------------------
# Deserialize the retrieved data from the DB
# -------------------------------------------------------------------------------
def utils_deserialize_data(db_data):
    glogger.info("Deserialize: DBData=%s", db_data)
    data_bytes = base64.b64decode(db_data)
    user_data = data_bytes.decode('ascii')
    glogger.info("Deserialize: DBData=%s UserData=%s", db_data, user_data)
    return user_data


# -------------------------------------------------------------------------------
# Clone an object
# -------------------------------------------------------------------------------
def utils_deep_copy(src_obj):
    clone = copy.deepcopy(src_obj)
    return clone
