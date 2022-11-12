import ast
from flask import request
from common.util.logging_helper  import get_logger
from common.util.config_wrapper import config_is_debug_mode, config_log_request

# -----------------------------------
# Create an instrance of the logger
# -----------------------------------
glogger = get_logger("request")


# -----------------------------------------------------------------------------------------
# Get a parameter from the request (returns Response as a json when error & param value)
# -----------------------------------------------------------------------------------------
def request_get_param(param_name):
    if not request.args:
        glogger.error("Missing Parameter. Expected parameter: %s", param_name)
        return None
    param = request.args.get(param_name)
    if not param:
        glogger.error("Bad Parameter Error. Expected %s", param_name)
        return None
    glogger.debug("%s=%s", param_name, param)
    return param

# -----------------------------------------------------------------------------------------
# Get the data (as dictionary that was passed)
# -----------------------------------------------------------------------------------------
def request_get_dict_param(param_name):
    rxed_data = request_get_param(param_name)
    if rxed_data is None:
        return None
    try:
        dict_data = ast.literal_eval(rxed_data)
    except Exception as err:
        glogger.error("Invalid data format. Expected dictionary. Could not convert: %s. err=%s", param_name, err)
        return None
    if not isinstance(dict_data, dict):
        glogger.error("Invalid data format arrived. Expected dictionary. Received=%s", rxed_data)
        return None
    return dict_data

# -----------------------------------------------------------------------------------------
# Get file list parameter
# -----------------------------------------------------------------------------------------
def request_get_filelist_param():
    if not request.files:
        glogger.error("The files list is non in the request. Invalid files list.")
        return None
    files_ids = list(request.files)
    glogger.info("Number of uploaded files : %d", len(files_ids))
    return files_ids

# ---------------------------------
# Get the cookies
# ---------------------------------
def request_get_cookies():
    return request.cookies.get('session')

# ---------------------------------
# Print Request Info
# ---------------------------------
def request_print():
    if not config_log_request():
        return
    if config_is_debug_mode():  # Development Environment Only
        _request_full_print()
    else:
        glogger.info("URL=%s", request.url)

# ---------------------------------
# Check errors in the request  
# ---------------------------------
def request_check_is_error():
    if "error" in request.args:  # Authentication/Authorization failure
        glogger.error("There is an error in login. args=%s", request.args)
        return True
    return False

# ---------------------------------
# Print Full Request Info
# ---------------------------------
def _request_full_print():
    print("request.args: " + str(request.args))
    print("request.form: " + str(request.form))
    print("request.files: " + str(request.files))
    print("request.values: " + str(request.values))
    #print("request.json: " + str(request.json))

    glogger.info("IsError=%s", request_check_is_error())
    glogger.info("Path=%s", request.path)
    glogger.info("FullPath=%s", request.full_path)
    glogger.info("ScriptRoot=%s", request.script_root)
    glogger.info("BaseURL=%s", request.base_url)
    glogger.info("URL=%s", request.url)
    glogger.info("URLRoot=%s", request.url_root)
    glogger.info("State=%s", request.args.get('state'))
    #glogger.info("Cookies: %s", request.cookies)
    if request.args:
        glogger.info("Request Code: %s", str(request.args.get('code')))
        glogger.info("Request Args: %s", request.args)
    else:
        glogger.info("Request Args: None")
    if request.files:
        glogger.info("Files: %s", list(request.files))
    else:
        glogger.info("Files: None")
    glogger.debug("Request=%s", request)

# ---------------------------------
# Get post parameter as a json
# ---------------------------------
def request_post_params_as_json():
    try:
        request_data = request.get_json()
    except Exception as err:
        glogger.error("Failed to get the POST parameters as JSON")
        return None
    return request_data