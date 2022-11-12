# import ast
from flask import jsonify
from flask import make_response
# from flask_pyjwt import current_token
from auth.auth import *
from common.controllers.contract import DocuSignContractHelper, Contract
from common.util.config_wrapper import *
#from common.util.filesop import *
from common.models.fs_files import *
# from models.image import *
from proxy.request_helper import *
from proxy.session import *
from common.util.logging_helper import get_logger
from common.util.utility_functions import utils_is_dev_env
from common.util.performance import performance_start_timer, performance_print_took_time
# from database.db_user_data import *
from common.kv.kv_helper import *
from common.controllers.dbhandles import *
# from bankapi.controllers.bankapi import *
from proxy.usertype import UserType
from common.controllers.fee import *
# from common.activedir.activedir_wrapper import *
from common.msgraph.msgraphapp import *
from newuser.newuser import *
from common.models.calculate_payout import *
from common.controllers.contract import send_promotion_to_client
from  common.controllers.contract_storage import *
from  common.controllers.logfiles_storage import *
from  common.models.db_files import *


# -------------------------------------------------------------
# Class Proxy
# -------------------------------------------------------------
class Proxy:
    _version = "0.128"  # The version of the API WEB application
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if Proxy.__instance is None:
            Proxy()
        return Proxy.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
        if Proxy.__instance != None:
            raise Exception("This class (Proxy) is a singleton!")
            return
        Proxy.__instance = self
        self.glogger = get_logger("Proxy")
        self.glogger.debug("Creating the instance of Proxy")
        self.dbhandles = Dbhandles.get_instance()  # Get the instance of the dbhandles

        # ------------------------------------------------------------------------------------
        # Any Jump table (APIs that can be called by any one - even if he is not a client yet)
        # The Jump-Table fields: Function, Type, LoggedUser
        # Function - The name of the function to be invoked
        # Type - Is it a STREAM function (like log) or returns Json
        # LoggedUser - This function must be called after login (True)
        # ------------------------------------------------------------------------------------
        self.jumptable = {
            'emailexists': (self._emailexists, None, False, "any"),  #
            'geturl': (self._geturl, None, False, "any"),  #
            'loginfail': (self._loginfail, None, False, "any"),  #
            'loginok': (self._loginok, None, False, "any"),  #
            'logout': (self._logout, None, False, "any"),  #
            'getinfo': (self._getinfo, None, True, "any"),  #
            'gettockeninfo': (self._gettockeninfo, None, False, "any"),
            'addnewuser': (self._addnewuser, None, False, "any"),  #
            'simulate-prospect-planner': (self._simulate_prospect, None, False, "any"),  #
            # Streaming - Need to be moved to ADMIN jump table

            'deleteuser': (self._deleteuser, None, True, "client"),  # move to admin ?
            'activateuser': (self._activateuser, None, True, "client"),  # move to admin ?
            'deactivateuser': (self._deactivateuser, None, True, "client"),  # move to admin ?
            'setparent': (self._setparent, None, True, "client"),  # move RIA
            'getmychildren': (self._getmychildren, None, True, "client"),  # move to RIA
            'depoistmoney': (self._depoistmoney, None, True, "client"),  # move RIA
            'withdrawalmoney': (self._withdrawalmoney, None, True, "client"),  # RIA
            'depositcomplete': (self._depositcomplete, None, True, "client"),  # RIA
            'withdrawalpending': (self._withdrawalpending, None, True, "client"),  # RIA
            'withdrawalcomplete': (self._withdrawalcomplete, None, True, "client"),  # RIA
            'getaccountid': (self._getaccountid, None, True, "client"),  #
            'getuserpii': (self._getuserpii, None, True, "client"),  #
            'userdata': (self._userdata, None, True, "client"),
            'bankapihook_corp': (self._bankapihook_corp, 'STREAM', False, "client"),  #
            'bankapihook_savvly': (self._bankapihook_savvly, 'STREAM', False, "client"),  #
            # 'userdatadiag'            : (self._userdata, None, False, "client"),                    #
            'transactions': (self._transactions, None, True, "client"),  #
            'userbalance': (self._userbalance, None, True, "client"),  #
            # 'setdefaultimage'         : (self._setdefaultimage, None, False, "client"),          #
            # 'deleteimage'             : (self._deleteimage, None, False, "client"),                  #
            # 'downloadimage'           : (self._downloadimage, 'STREAM', True, "client"),           # Streaming + Logged-in

            # 'createuserhandle'        : (self._createuserhandle, None, False, "client"),        #

            'uploadfile2fs': (self._uploadfile2fs, None, False, "advisor"),      #
            'uploadcontract': (self._uploadcontract, None, True, "advisor"),       #
            'listdbfiles': (self._listdbfiles, None, False, "admin"),             #
            'deletedbfile': (self._deletedbfile, None, False, "admin"),  #
            'listfsfiles': (self._listfsfiles, None, False, "admin"),            #
            'deletefsfile': (self._deletefsfile, None, False, "admin"),          #
            'downloadfsfile': (self._downloadfsfile, 'STREAM', False, "admin"),  # Streaming
            'downloadlogfile': (self._downloadlogfile, 'STREAM', False, "any"),  # @2do: Change to Admin
            'uploadlogfile': (self._uploadlogfile, None, False, "any"),          # @2do: Change to Admin

            'isadvisor': (self._isadvisor, None, True, "advisor"),
            'getadvisorinfo': (self._getadvisorinfo, None, True, "advisor"),
            'addchild': (self._addchild, None, True, "advisor"),
            'getadvisorchildren': (self._getadvisorchildren, None, True, "advisor"),
            'delchild': (self._delchild, None, True, "advisor"),
            'getadvisorchildrenstatus': (self._getadvisorchildrenstatus, None, True, "advisor"),
            'addpotentialclient': (self._addpotentialclient, None, True, "advisor"),
            'getpotentialclients': (self._getpotentialclients, None, True, "advisor"),

            'previewcontract': (self._previewcontract, 'STREAM', True, "advisor"),
            'docusignretrieve': (self._docusignretrieve, 'STREAM', True, "advisor"),
            'docusigninfo': (self._docusigninfo, None, True, "advisor"),

            'sendcontract': (self._sendcontract, None, True, "validatedadvisor"),
            'updatecontractstatus': (self._updatecontractstatus, None, True, "validatedadvisor"),

            'environment': (self._set_environment, None, True, "admin"),  #
            'users': (self._users, None, True, "admin"),  #
            'accountids': (self._accountids, None, True, "admin"),  #
            'statuses': (self._statuses, None, True, "admin"),  #
            'fmvs': (self._fmvs, None, True, "admin"),  #
            'usertablesdiag': (self._usertablesdiag, None, True, "admin"),  #
            'usersdata': (self._usersdata, None, True, "admin"),  #
            # 'deleteallusers'          : (self._deleteallusers, None, False, "admin"),        #
            'deleteusertables': (self._deleteusertables, None, True, "admin"),  #
            'deletealltables': (self._deletealltables, None, True, "admin"),




            'alltablenames': (self._alltablenames, None, True, "admin"),  #
            'addnewcolumn': (self._addnewcolumn, None, True, "admin"),  #
            # 'userimage': (self._userimage, 'STREAM', False, "admin"),              # Streaming
            # 'doaction': (self._doaction, None, False, "admin"),                    #
            # 'imagessize': (self._imagessize, None, False, "admin"),                #
            # 'schema': (self._schema, None, False, "admin"),                        #
            # 'schemascope': (self._schemascope, None, False, "admin"),              #
            'getallkv': (self._getallkv, None, True, "admin"),  #
            'delallkv': (self._delallkv, None, True, "admin"),  #
            'initkv': (self._initkv, None, True, "admin"),  #
            'getadmins': (self._getadmins, None, True, "admin"),  #
            'addadmin': (self._addadmin, None, True, "admin"),  #
            'deladmin': (self._deladmin, None, True, "admin"),  #

            'deductmngfee': (self._deductmngfee, None, True, "admin"),  #
            'deductsignfee': (self._deductsignfee, None, True, "admin"),  #
            'deductmiscfee': (self._deductmiscfee, None, True, "admin"),  #
            # 'updateriadata': (self._updateriadata, None, True, "admin"),  # update database functions
            'updateuserdata': (self._updateuserdata, None, True, "admin"),  #
            'updateuserdata2': (self._updateuserdata2, None, True, "admin"),  #
            'updatedailydata': (self._updatedailydata, None, True, "admin"),  #
            'getusersinfo': (self._getusersinfo, None, True, "admin"),  # Active Directory APIs
            'getusersemail': (self._getusersemail, None, True, "admin"),  #
            'createuser': (self._createuser, None, True, "admin"),  #
            'addnewadvisor': (self._addnewadvisor, None, True, "admin"),  # Advisors
            'validateadvisor': (self._validateadvisor, None, True, "admin"),
            'deleteadvisor': (self._deleteadvisor, None, True, "admin"),
            'getallassociatedrias': (self._getallassociatedrias, None, True, "admin"),
            'getsignedcontracts': (self._getsignedcontracts, None, True, "admin"),

            'userschangefeed': (self._userschangefeed, None, True, "admin"),
            'advisorschangefeed': (self._advisorschangefeed, None, True, "admin"),
            'potentialschangefeed': (self._potentialschangefeed, None, True, "admin"),

            'getoldpotentials': (self._getoldpotentials, None, True, "admin"),
            'deloldpotentials': (self._deloldpotentials, None, True, "admin"),

            'getusercontracts': (self._getusercontracts, None, True, "admin"),
            'addusercontract': (self._addusercontract, None, True, "admin"),

        }

    # -----------------------------------
    # Run a function
    # -----------------------------------
    def run(self, func_name):
        request_print()
        session_print()
        start_time = performance_start_timer()
        response = self._run(func_name)
        if isinstance(response, dict):
            duration = performance_print_took_time(f"%s" % func_name, start_time)
            self._add_tooktime_to_response(response, duration)
            self.glogger.debug("Request: %s Response=%s", func_name, str(response))
            json_response = jsonify(response)
            resp = make_response(json_response)
            self.glogger.debug("Returning from Run")
            # print(resp)
            return resp
        else:
            return response  # Stream back the data

    # -----------------------------------
    # Run a function
    # -----------------------------------
    def _run(self, func_name):
        response = {}
        func_info = self._find_func(func_name)
        if not func_info:
            # self._prepare_response_error(response, "Invalid " + func_name)
            return self._invalid_api(func_name)
        func = func_info[0]  # The function itself
        functype = func_info[1]  # The type of the function
        by_logged_user_only = func_info[2]  # The operation is allowed by the logged user only
        api_allowed_by = func_info[3]  # The operation is allowed by the specific type of users
        response = self._prepare_response_basic(func_name)
        if not self._verify_user_logged_in(response, by_logged_user_only):
            self._set_opertaion_result(response, "Fail")
            return response
        if not self._is_api_allowed_by_user_type(func_name, by_logged_user_only, api_allowed_by):
            self._set_opertaion_result(response, "Not Allowed")
            self._add_item_to_response(response, 'api_allowed_by', api_allowed_by)
            return response
        self._add_item_to_response(response, 'logged-userid', auth_get_current_userid())
        try:
            result = func()
            if result:
                if functype == 'STREAM':
                    self.glogger.info("The function %s is streaming its data back to the client", func_name)
                    return result  # This function is streaming its data back
                response.update(result)
            else:
                self.glogger.error("The function %s did not return a valid response", func_name)
                self._set_opertaion_result(response, "Fail")
        except Exception as err:
            self.glogger.error("The function %s got an exception. err=%s", func_name, err)
            self._set_opertaion_result(response, "Exception")
            self._add_item_to_response(response, 'Exception', str(err))
        return response

    # ---------------------------------------
    # Invalid API passed - Retun a response
    # ---------------------------------------
    def _invalid_api(self, func_name):
        self.glogger.error("Invalid API request : %s", func_name)
        response = self._prepare_response_basic(func_name)
        self._prepare_response_error(response, "Invalid API-" + func_name)
        return response

    # -----------------------------------
    # Find a function from the jump-table
    # -----------------------------------
    def _find_func(self, func_name: str):
        self.glogger.debug("Looking for function=%s in the jump-tables", func_name)
        func_info = self.__find_func(func_name, self.jumptable)
        if func_info:
            self.glogger.debug("The function=%s found in the jump-table", func_name)
            return func_info
        self.glogger.error("function name %s not found in the jump-tables", func_name)
        return None

        # self.glogger.debug("Looking for function=%s in the jump-tables", func_name)
        # user_type = session_get_user_type()
        # if user_type == "savvlyclient" or user_type == "savvlyadmin" or user_type == "savvlyadvisor" or user_type is None:
        #    func_info = self.__find_func(func_name, self.any_jumptable)
        #    if func_info:
        #        self.glogger.debug("The function=%s found in the jump-table ANY (user_type=%s)", func_name, user_type)
        #        return func_info

    #
    # if user_type == "savvlyclient" or user_type == "savvlyadmin" or user_type == "savvlyadvisor":
    #    func_info = self.__find_func(func_name, self.user_jumptable)
    #    if func_info:
    #        self.glogger.debug("The function=%s found in the jump-table USER (user_type=%s)", func_name, user_type)
    #        return func_info
    #
    # if user_type == "savvlyadmin" or user_type == "savvlyadvisor":
    #    func_info = self.__find_func(func_name, self.RIA_jumptable)
    #    if func_info:
    #        self.glogger.debug("The function=%s found in the jump-table RIA (user_type=%s)", func_name, user_type)
    #        return func_info
    #
    # if user_type == "savvlyadmin":
    #    func_info = self.__find_func(func_name, self.admin_jumptable)
    #    if func_info:
    #        self.glogger.debug("The function=%s found in the jump-table ADMIN (user_type=%s)", func_name, user_type)
    #        return func_info
    #
    # self.glogger.error("function name %s not found in the jump-tables (user_type=%s)", func_name, user_type)
    # return None

    # ----------------------------------------------------------
    # Check if the operation is allowed by the user type
    # api_allowed_by: "any", "client", "advisor", "admin"
    # ----------------------------------------------------------
    def _is_api_allowed_by_user_type(self, func_name, by_logged_user_only, api_allowed_by: str):
        if not by_logged_user_only:
            return True  # No logged user is required to run the API
        user_type = session_get_user_type()
        if user_type is None or api_allowed_by is None:
            self.glogger.error("Invalid user-type=%s or api-type=%s. cannot check permission", user_type,
                               api_allowed_by)
            return False
        if api_allowed_by == "any":
            return True  # Anyone can run this API
        if user_type == "savvlyadmin":
            return True  # Admin can run every API
        client_apis = ["client"]
        advisor_apis = ["client", "advisor"]
        validated_advisor_apis = ["client", "advisor", "validatedadvisor"]

        if user_type == "savvlyclient" and api_allowed_by in client_apis:
            return True  # The client can run client API only
        if user_type == "savvlyadvisor" and api_allowed_by in advisor_apis:
            return True  # a non-validated advisor can run everything, except admin and validated-advisor
        if user_type == "savvlyvalidatedadvisor" and api_allowed_by in validated_advisor_apis:
            return True  # a non-validated advisor can run everything, except admin and validated-advisor
        self.glogger.error("The API (%s) is allowed by %s, but the logged in user type is: %s", func_name,
                           api_allowed_by, user_type)
        return False

    # -----------------------------------
    # Find a function from the jump-table
    # -----------------------------------
    def __find_func(self, func_name: str, jumptable: dict):
        for name, func_info in jumptable.items():
            if name == func_name:
                return func_info
        return None

    # -----------------------------------
    # Verify that the user is logged-in
    # -----------------------------------
    def _verify_user_logged_in(self, response, by_logged_user_only):
        if not by_logged_user_only:
            return True  # Any user can do this operation
        if auth_get_current_userid():
            return True  # The user is already logged-in
        parsed_token = auth_parse_access_token()
        if parsed_token is None:
            self._add_item_to_response(response, 'Error',
                                       "No token access found in the header. This API requires access token")
            self._set_opertaion_result(response, 'Fail')
            return False  # The user is not logged-in
        if not auth_get_current_userid():
            self._add_item_to_response(response, 'Error', "No user is logged-in. This operation is not allowed")
            self._set_opertaion_result(response, 'Fail')
            return False  # The user is not logged-in
        result = self._process_logged_in_user(auth_get_current_userid())
        return result  # The user is logged-in

    # -----------------------------------
    # Add item to the response
    # -----------------------------------
    def _add_item_to_response(self, response, key: str, value):
        response[key] = value

    # -----------------------------------
    # Prepare Response: add passed-userid
    # -----------------------------------
    def _add_userid_to_response(self, response, userid):
        self._add_item_to_response(response, 'userid', userid)

    # -----------------------------------
    # Prepare Response: Basic (Common)
    # -----------------------------------
    def _prepare_response_basic(self, func_name):
        response = {}
        self._add_item_to_response(response, 'API', func_name)
        self._add_item_to_response(response, 'version', self._get_version())
        self._add_item_to_response(response, 'logged-userid', auth_get_current_userid())
        self._set_opertaion_result(response, 'OK')
        return response

    # -----------------------------------
    # Prepare Response: Error
    # -----------------------------------
    def _prepare_response_error(self, response, resultcode):
        self._set_opertaion_result(response, 'Fail')
        self._add_item_to_response(response, 'code', resultcode)
        return response

    # ----------------------------------------
    # Prepare DB connectivity response
    # ----------------------------------------
    def _prepare_bad_db_connection_response(self):
        response = {}
        self._add_item_to_response(response, 'Error', "Failed to access DB. Probably DB server is down or unreachable")
        return response

    # -----------------------------------
    # Set proxy operation result
    # -----------------------------------
    def _set_opertaion_result(self, response, result: str):
        self._add_item_to_response(response, 'proxyres', result)

    # -----------------------------------
    # Add took time to the response
    # -----------------------------------
    def _add_tooktime_to_response(self, response, duration: str):
        self._add_item_to_response(response, 'tooktime', duration)

    # -----------------------------------------------------------------------------------------
    # Get a parameter from the request (returns Response as a json when error & param value)
    # -----------------------------------------------------------------------------------------
    def _get_param(self, param_name):
        value = request_get_param(param_name)
        if value is None:
            response = {}
            self._prepare_response_error(response, "bad-param-" + param_name)
            return response, None
        return None, value

    # -----------------------------------------------------------------------------------------
    # Get the userid parameter from the request (returns Response as a json when error & param value)
    # In admin mode: The passed userid 'wins'
    # In normal mode: The logged-in userid 'wins'
    # -----------------------------------------------------------------------------------------
    def _get_userid_param(self):
        isdmin = config_is_admin_mode()
        logged_in_userid = auth_get_current_userid()
        response, passed_userid = self._get_param('userid')
        if response:
            return response, None
        if isdmin == True and passed_userid is not None:
            self.glogger.info("Admin; Passed userid by API; userid: %s", passed_userid)
            return None, passed_userid
        if isdmin == False and logged_in_userid is not None:
            self.glogger.info("Not-Admin; User is Logged-in; userid: %s", logged_in_userid)
            return None, logged_in_userid
        if isdmin == False and logged_in_userid is None:
            self.glogger.info("Not-Admin; No user is logged-in; userid: None")
            return response, None
        return None, logged_in_userid

    # -----------------------------------------------------------------------------------------
    # Get the username (user handle) parameter
    # -----------------------------------------------------------------------------------------
    def _get_userhandle_param(self):
        response, userhandle = self._get_param('userhandle')
        if response:
            return response, None
        return None, userhandle

    # -----------------------------------------------------------------------------------------
    # Get the data (as dictionary that was passed)
    # -----------------------------------------------------------------------------------------
    def _get_dict_param(self, param_name):
        dict_data = request_get_dict_param(param_name)
        if dict_data is None:
            response = {}
            self._prepare_response_error(response, "bad-param-" + param_name)
            return response, None
        return None, dict_data

    # -----------------------------------------------------------------------------------------
    # Get the data (as dictionary that was passed)
    # -----------------------------------------------------------------------------------------
    def _get_data_dict_param(self):
        return self._get_dict_param('data')

    # -----------------------------------------------------------------------------------------
    # Get a passed integer
    # -----------------------------------------------------------------------------------------
    def _get_int_param(self, param_name):
        response, rxed_data = self._get_param(param_name)
        if response:
            return response, None
        try:
            int_value = int(rxed_data)
        except Exception as err:
            response = {}
            self.glogger.error("Invalid data format. Expected Integer. Could not convert: %s. err=%s", param_name, err)
            self._set_opertaion_result(response, "Exception")
            self._add_item_to_response(response, 'Exception', str(err))
            return response, None
        return None, int_value

    # -----------------------------------------------------------------------------------------
    # Get a passed Float
    # -----------------------------------------------------------------------------------------
    def _get_float_param(self, param_name):
        response, rxed_data = self._get_param(param_name)
        if response:
            return response, None
        return self._validate_float_param(rxed_data)

    # -----------------------------------------------------------------------------------------
    # Get a passed table number
    # -----------------------------------------------------------------------------------------
    def _get_table_param(self):
        return self._get_param('table')

    # -----------------------------------------------------------------------------------------
    # Validate passed float number
    # -----------------------------------------------------------------------------------------
    def _validate_float_param(self, fltnum: float):
        try:
            floatnum = float(fltnum)
        except Exception as err:
            response = {}
            self.glogger.error("The format of the fltnum:%s is invalid. It must be a (float) number", fltnum)
            self._set_opertaion_result(response, "Exception")
            self._add_item_to_response(response, 'Exception', str(err))
            return response, None
        return None, floatnum

    # -----------------------------------------------------------------------------------------
    # Get a passed amount (returns Float number)
    # -----------------------------------------------------------------------------------------
    def _get_amount_param(self):
        response, amount = self._get_param('amount')
        if response:
            return response, None
        response, amount_num = self._validate_float_param(amount)
        if response:
            return response, None
        return None, amount_num

    # -----------------------------------------------------------------------------------------
    # Get a passed Share Cost (returns Float number)
    # -----------------------------------------------------------------------------------------
    def _get_sharecost_param(self):
        response, share = self._get_param('share')
        if response:
            return response, None
        response, share_num = self._validate_float_param(share)
        if response:
            return response, None
        return None, share_num

    # -----------------------------------------------------------------------------------------
    # Get file list parameter
    # -----------------------------------------------------------------------------------------
    def _get_filelist_param(self):
        files_ids = request_get_filelist_param()
        if files_ids is None:
            response = {}
            self._prepare_response_error(response, "bad-param-files")
            return response, None
        return None, files_ids

    # -----------------------------------
    # Get Info
    # -----------------------------------
    def _getinfo(self):
        # user_id = session_get_user_id()
        is_devmode = config_is_dev_mode()
        response = {}
        self._add_item_to_response(response, 'isdev', is_devmode)
        self._add_item_to_response(response, 'isdebug', config_is_debug_mode())
        self._add_item_to_response(response, 'isdmin', config_is_admin_mode())
        self._add_item_to_response(response, 'logcmd', config_log_cql_commands())
        self._add_item_to_response(response, 'logres', config_log_cql_results())
        self._add_item_to_response(response, 'dbname', dbwrapper_get_db_keyspace_name())
        self._getuserinfo(response)
        if is_devmode:
            self._add_item_to_response(response, 'cookies', request_get_cookies())
        return response

    # -----------------------------------
    # Get token Info
    # -----------------------------------
    def _gettockeninfo(self):
        response = {}
        self._add_item_to_response(response, 'token_type', current_token.token_type)
        self._add_item_to_response(response, 'subject', current_token.sub)
        self._add_item_to_response(response, 'scope', current_token.scope)
        self._add_item_to_response(response, 'claims', current_token.claims)
        self._add_item_to_response(response, 'is_signed', current_token.is_signed())
        self._add_item_to_response(response, 'signed_token', current_token.signed)
        return response

    # -----------------------------------
    # Get a specific url
    # -----------------------------------
    def _geturl(self):
        response, urltype = self._get_param('type')
        if response:
            return response
        url = None
        if urltype == 'login':
            url = auth_get_login_url()
        elif urltype == 'regadvisor':
            url = get_register_advisor_url()
        elif urltype == 'reguser':
            url = get_register_user_url()
        else:
            self.glogger.info("Invalid url-type requested: %s (valid: login, regadvisor, reguser)", urltype)
        response = {}
        self._add_item_to_response(response, 'url', url)
        return response

    # -----------------------------------
    # Login Failed
    # -----------------------------------
    def _loginfail(self):
        response = {}
        self._set_opertaion_result(response, "Fail")
        self._add_item_to_response(response, 'login', "Fail")
        return response

    # -----------------------------------
    # Login OK
    # -----------------------------------
    def _loginok(self):
        logged_user_id = auth_get_current_userid()
        result = self._process_logged_in_user(logged_user_id)
        # session_print()
        response = {}
        self._add_item_to_response(response, 'login', "OK")
        self._add_item_to_response(response, 'postloginresult', result)
        self._getuserinfo(response, auth_get_current_userid())
        return response

    # -----------------------------------
    # Logout
    # -----------------------------------
    def _logout(self):
        auth_post_logout()
        response = {}
        self._add_item_to_response(response, 'logout', "OK")
        return response

    # -----------------------------------
    # Set Environment
    # -----------------------------------
    def _set_environment(self):
        response, isdev = self._get_param('dev')
        if response:
            return response
        response, debug = self._get_param('debug')
        if response:
            return response
        response, logcmd = self._get_param('logcmd')
        if response:
            return response
        response, logres = self._get_param('logres')
        if response:
            return response
        response, isadmin = self._get_param('admin')
        if response:
            return response
        response, logsess = self._get_param('logsess')
        if response:
            return response
        response, logreq = self._get_param('logreq')
        if response:
            return response
        response = {}

        if isdev == '1':
            config_set_dev_mode(True)  # Set Development Environment ON
        elif isdev == '0':
            config_set_dev_mode(False)  # Set Development Environment OFF
        else:
            self.glogger.info("The IsDev did not change: %s", isdev)
            self._add_item_to_response(response, 'dev', "Invalid")

        if debug == '1':
            config_set_debug_mode(True)  # Set Debug ON
        elif debug == '0':
            config_set_debug_mode(False)  # Set Debug OFF
        else:
            self.glogger.info("The DEBUG did not change: %s", debug)
            self._add_item_to_response(response, 'debug', "Invalid")

        if logcmd == '1':
            config_set_log_cql_commands(True)  # Print/Log CQL query commands
        elif logcmd == '0':
            config_set_log_cql_commands(False)  # Do not Print/Log CQL query commands
        else:
            self.glogger.info("The logcmd did not change: %s", logcmd)
            self._add_item_to_response(response, 'logcmd', "Invalid")

        if logres == '1':
            config_set_log_cql_results(True)  # Print/Log CQL query Results
        elif logres == '0':
            config_set_log_cql_results(False)  # Do not Print/Log CQL query Results
        else:
            self.glogger.info("The logres did not change: %s", logres)
            self._add_item_to_response(response, 'logres', "Invalid")

        if isadmin == '1':
            config_set_admin_mode(True)  # This is admin mode
        elif isadmin == '0':
            config_set_admin_mode(False)  # This is not admin mode
        else:
            self.glogger.info("The admin did not change: %s", isadmin)
            self._add_item_to_response(response, 'admin', "Invalid")

        if logsess == '1':
            config_set_log_session(True)  # Start logging the session
        elif logsess == '0':
            config_set_log_session(False)  # Do not log sessions
        else:
            self.glogger.info("The logsess did not change: %s", logsess)
            self._add_item_to_response(response, 'logsess', "Invalid")

        if logreq == '1':
            config_set_log_request(True)  # Start logging the request
        elif logreq == '0':
            config_set_log_request(False)  # Do not log request
        else:
            self.glogger.info("The logreq did not change: %s", logreq)
            self._add_item_to_response(response, 'logreq', "Invalid")

        self._add_item_to_response(response, 'dev', config_is_dev_mode())
        self._add_item_to_response(response, 'debug', config_is_debug_mode())
        self._add_item_to_response(response, 'logcmd', config_log_cql_commands())
        self._add_item_to_response(response, 'logres', config_log_cql_results())
        self._add_item_to_response(response, 'admin', config_is_admin_mode())
        self._add_item_to_response(response, 'logsess', config_log_session())
        self._add_item_to_response(response, 'logreq', config_log_request())

        return response

    # ----------------------------------------
    # Get the list of the users
    # ----------------------------------------
    def _users(self):
        return self._doaction_on_usertables_all('get_idx_list', 'users')

    # ----------------------------------------
    # Get all the users
    # ----------------------------------------
    def _usersdata(self):
        return self._doaction_on_usertables_all('get_all_tables', 'usersdata')

    # ----------------------------------------
    # Get change feeds of the user tables
    # ----------------------------------------
    def _userschangefeed(self):
        response, start_date_time = self._get_param('start')
        if response:
            return response
        return self._doaction_on_usertables_all_single_param('get_all_change_feeds', 'userschangesfeed',
                                                             start_date_time)

    # ----------------------------------------
    # Get all the users account IDs
    # ----------------------------------------
    def _accountids(self):
        return self._doaction_on_usertables_all('get_all_accountids', 'acountids')

    # ----------------------------------------
    # Get all the users status
    # ----------------------------------------
    def _statuses(self):
        return self._doaction_on_usertables_all('get_all_statuses', 'statuses')

    # ----------------------------------------
    # Get all the users FMV
    # ----------------------------------------
    def _fmvs(self):
        return self._doaction_on_usertables_all('get_all_fmvs', 'fmvs')

    # ----------------------------------------
    # Get all contracts from the user tables
    # ----------------------------------------
    def _getsignedcontracts(self):
        return self._doaction_on_usertables_all('get_all_contracts', 'contracts')

    # ----------------------------------------
    # Delete all the users
    # ----------------------------------------
    def _deleteallusers(self):
        response = {}
        count = self.dbhandles.get_usertables().delete_all_idx()
        if count < 0:
            return self._prepare_bad_db_connection_response()
        self._add_item_to_response(response, 'deleteallusers', str(count))
        return response

    # ----------------------------------------
    # Delete all the user Tables
    # ----------------------------------------
    def _deleteusertables(self):
        response = {}
        self.dbhandles.delete_user_tables()
        self._add_item_to_response(response, 'deleteusertables', "dropped")
        return response

    # ----------------------------------------
    # Delete all tables from the database
    # ----------------------------------------
    def _deletealltables(self):
        response = {}
        self.dbhandles.delete_all_tables()
        self._add_item_to_response(response, 'deletealltables', "dropped")
        return response

    # ----------------------------------------
    # Get the names of all tales in the schemma
    # ----------------------------------------
    def _alltablenames(self):
        table_list = self.dbhandles.get_usertables().get_keyspace_tables_names()
        if table_list is None:
            return self._prepare_bad_db_connection_response()
        response = {}
        self._add_item_to_response(response, 'alltablenames', table_list)
        return response

    # ----------------------------------------
    # Add a new column to a table
    # ----------------------------------------
    def _addnewcolumn(self):
        response, tablename = self._get_param('tablename')
        if response:
            return response
        response, colname = self._get_param('colname')
        if response:
            return response
        response = {}
        self._add_item_to_response(response, 'addnewcolumn', table_list)
        return response

    # ----------------------------------------
    # Add a new user
    # ----------------------------------------
    def _addnewuser(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        response, userinfo = self._get_dict_param('userinfo')
        if response:
            return response
        self.dbhandles.get_usertables().add_new_user(userid, userinfo)
        response = {}
        self._add_item_to_response(response, 'addnewuser', str(userid))
        return response

    # ----------------------------------------
    # Add a new potential client
    # ----------------------------------------
    def _addpotentialclient(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        response, email = self._get_param('email')
        if response:
            return response
        # response, contractid = self._get_param('contractid')
        # if response:
        #     return response
        response, clientinfo = self._get_dict_param('clientinfo')
        if response:
            return response

        ret = self.dbhandles.get_potential_clients_tables().add_new_client(advisor_id, email, clientinfo)

        response = {}
        if not ret:
            self._add_item_to_response(response, "result", "failed")
        else:
            self._add_item_to_response(response, 'addpotentialclient', email)
        return response

    # ----------------------------------------
    # Get potential clients/contracts list by status
    # ----------------------------------------
    def _getpotentialclients(self):
        # response, advisor_id = self._get_userid_param()
        # if response:
        #    return response
        response, status = self._get_param('status')
        if response:
            return response
        return self._doaction_on_potentialtables_two_params("get_all_clients_by_status", 'potentialclients', status)

        # rows = self.dbhandles.get_potential_clients_tables().get_all_clients_by_status(advisor_id, status)
        # response = {}
        # self._add_item_to_response(response, 'getpotentialclients', rows)
        # return response

    # ----------------------------------------
    # Get old potential clients/contracts list by status (for admin only over all table)
    # ----------------------------------------
    def _getoldpotentials(self):
        response, status = self._get_param('status')
        if response:
            return response

        response, days = self._get_int_param('days')
        if response:
            return response

        rows = self.dbhandles.get_potential_clients_tables().delete_old_records(status=status, days_thresh=days,
                                                                                do_delete=False)
        response = {}
        self._add_item_to_response(response, 'getoldpotentials', rows)
        return response

    # ----------------------------------------
    # Delete old potential clients/contracts list by status (for admin only over all table)
    # ----------------------------------------
    def _deloldpotentials(self):
        response, status = self._get_param('status')
        if response:
            return response

        response, days = self._get_int_param('days')
        if response:
            return response

        rows = self.dbhandles.get_potential_clients_tables().delete_old_records(status=status, days_thresh=days,
                                                                                do_delete=True)
        response = {}
        self._add_item_to_response(response, 'deloldpotentials', rows)
        return response

    # ----------------------------------------
    # Get change feeds of the potential tables
    # ----------------------------------------
    def _potentialschangefeed(self):
        response, start_date_time = self._get_param('start')
        if response:
            return response
        return self._doaction_on_potentialtables_all_single_param('get_all_change_feeds', 'potentialchangesfeed',
                                                                  start_date_time)

    # ----------------------------------------
    # Set potential contracts status
    # ----------------------------------------
    def _updatecontractstatus(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        response, email = self._get_param('email')
        if response:
            return response

        response, status = self._get_param('status')
        if response:
            return response
        # parameter validation status (updated in the set_client_status func)

        rows = self.dbhandles.get_potential_clients_tables().set_client_status(advisor_id, email, status)
        response = {}
        self._add_item_to_response(response, 'set_client_status', rows)
        return response

    # ----------------------------------------
    # sendcontract
    # ----------------------------------------
    def _sendcontract(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        response, email = self._get_param('email')
        if response:
            return response

        # contract_id = None - do not change contract id , it should be already set in create new potential client
        contract_id = send_promotion_to_client(advisor_id, email)
        # contract_id = self.dbhandles.get_potential_clients_tables().send_promotion_to_client(advisor_id, email)
        response = {}
        self._add_item_to_response(response, 'sendcontract', contract_id)
        return response

    # ----------------------------------------
    # Add a new potential client
    # ----------------------------------------
    def _previewcontract(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        response, email = self._get_param('email')
        if response:
            return response
        # response, contractid = self._get_param('contractid')
        # if response:
        #     return response
        response, client_info = self._get_dict_param('clientinfo')
        if response:
            return response

        # ret = self.dbhandles.get_potential_clients_tables().add_new_client(advisor_id, email, clientinfo)

        contract = Contract(email, client_info=client_info)

        ret = contract.preview_contract()

        response = {}
        if not ret:
            self._add_item_to_response(response, "result", "failed")
        else:
            self._add_item_to_response(response, 'previewcontract', 'OK')
        return ret  # stream of PDF contract

    # ----------------------------------------
    # retrieve contract from docusign
    # ----------------------------------------
    def _docusignretrieve(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        response, contract_id = self._get_param('contractid')
        if response:
            return response

        contract = DocuSignContractHelper(contract_id)

        ret = contract.retrieve_contract()

        response = {}
        if not ret:
            self._add_item_to_response(response, "result", "failed")
        else:
            self._add_item_to_response(response, 'previewcontract', 'OK')
        return ret  # stream of PDF contract

    # ----------------------------------------
    # retrieve contract info from docusign
    # ----------------------------------------
    def _docusigninfo(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        response, contract_id = self._get_param('contractid')
        if response:
            return response

        contract = DocuSignContractHelper(contract_id)

        ret = contract.contract_info()

        response = {}
        if not ret:
            self._add_item_to_response(response, "result", "failed")
        else:
            self._add_item_to_response(response, 'docusigninfo', 'OK')
        return ret  # docusign info

    # ----------------------------------------
    # validate an advisor
    # ----------------------------------------
    def _validateadvisor(self):
        response, is_validated = self._get_param('validated')
        if response:
            return response
        return self._doaction_on_riatables_two_params("set_is_validated", "validated", is_validated)

    # ----------------------------------------
    # Delete an advisor
    # ----------------------------------------
    def _deleteadvisor(self):
        response, advisor_id = self._get_userid_param()
        if response:
            return response
        MsGraphApp().delete_user(advisor_id)  # Delete the user from AAD
        return self._doaction_on_riatables_single_idx("delete_advisor", "deleteadvisor")  # Delete from DB

    # ----------------------------------------
    # Delete a user
    # ----------------------------------------
    def _deleteuser(self):
        response, user_id = self._get_userid_param()
        if response:
            return response
        MsGraphApp().delete_user(user_id)  # Delete the user from AAD
        return self._doaction_on_usertables_single_idx("delete_user", "deleteuser")

    # ----------------------------------------
    # Activate a user
    # ----------------------------------------
    def _activateuser(self):
        return self._doaction_on_usertables_single_idx("set_statusflag_active", "activateuser")

    # ----------------------------------------
    # Deactivate a user (dead)
    # ----------------------------------------
    def _deactivateuser(self):
        return self._doaction_on_usertables_single_idx("set_statusflag_deceased", "deactivateuser")

    # ----------------------------------------
    # Set Parent
    # ----------------------------------------
    def _setparent(self):
        response, parentid = self._get_param('parentid')
        if response:
            return response
        return self._doaction_on_usertables_two_params("set_parentid", "parent", parentid)

    # ----------------------------------------
    # Get My children
    # ----------------------------------------
    def _getmychildren(self):
        return self._doaction_on_usertables_single_idx("get_my_children", "mychildren")

    # ----------------------------------------
    # Deposit money to the user account
    # ----------------------------------------
    def _depoistmoney(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        response, amount = self._get_amount_param()
        if response:
            return response
        response, tran_id = self._get_param('tranid')
        if response:
            return response, None
        result = self.dbhandles.get_usertables().deposit_money(userid, amount, tran_id)
        self._process_user_deposits()  # Process the deposits
        response = {}
        self._add_item_to_response(response, 'depoistmoney', str(result))
        return response

    # ----------------------------------------
    # Withdrawal money to the user account
    # ----------------------------------------
    def _withdrawalmoney(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        response, amount = self._get_amount_param()
        if response:
            return response
        result = self.dbhandles.get_usertables().withdrawal_money(userid, amount)
        response = {}
        self._add_item_to_response(response, 'withdrawalmoney', str(result))
        return response

    # ----------------------------------------
    # Set Deposit completed
    # ----------------------------------------
    def _depositcomplete(self):
        return self._doaction_on_usertables_single_idx("set_statusflag_transfer_complete", "depositcomplete")

    # ----------------------------------------
    # Set Withdrawal pending
    # ----------------------------------------
    def _withdrawalpending(self):
        return self._doaction_on_usertables_single_idx("set_statusflag_withdrawal_pending", "withdrawalpending")

    # ----------------------------------------
    # Set Withdrawal completed
    # ----------------------------------------
    def _withdrawalcomplete(self):
        return self._doaction_on_usertables_single_idx("set_withdrawal_complete", "withdrawalcomplete")

    # ---------------------------------------------
    # Get the diagnostics of the users data tables
    # ----------------------------------------------
    def _usertablesdiag(self):
        response = {}
        user_data = self.dbhandles.get_usertables().get_diag(None)  # Pass None as userid to get
        self._add_item_to_response(response, 'usertablesdiag', user_data)
        return response

    # ----------------------------------------
    # Get the User's Account-ID
    # ----------------------------------------
    def _getaccountid(self):
        return self._doaction_on_usertables_single_idx("get_accountid", "getaccountid")

    # ----------------------------------------
    # Get the User's PII (user private info)
    # ----------------------------------------
    def _getuserpii(self):
        return self._doaction_on_usertables_single_idx("get_user_pii", "getuserpii")

    # ----------------------------------------
    # Get the data of a user
    # ----------------------------------------
    def _userdata(self):
        return self._doaction_on_usertables_single_idx("get_all_values", "userdata")

    # --------------------------------------------------------------------------
    # A callback function that is called by Bank API to notify about changes
    # The json format is: {"event": "ach.update", "op": "update", "id": "ach_01123456789", "url": "blabla"}
    # --------------------------------------------------------------------------
    def _bankapihook_process_data(self) -> bool:
        self.glogger.info("The callback function has been called by BankAPI")
        data_json = request_post_params_as_json()
        if not data_json:
            return False
        try:
            event = data_json["event"]
            op = data_json["op"]
            id = data_json["id"]
            url = data_json["url"]
            self.glogger.info("BankAPIHook: event=%s op=%s id=%s url=%s", event, op, id, url)
        except Exception as err:
            self.glogger.error("Invalid data received by BankAPIHook: %s", str(data_json))
            return False
        if event == "book.create" or event == "book.update" or event == "ach.create" or event == "ach.update":
            self.glogger.info("A an even came in: %s. A user has deposited some money", event)
            self._process_user_deposits()
        return True

    # --------------------------------------------------------------------------------------------
    # A callback function that is called by Bank API to notify about changes (Savvly Account)

    # --------------------------------------------------------------------------------------------
    def _bankapihook_savvly(self):
        result = self._bankapihook_process_data()
        if not result:
            return 'Internal Server Error', 500
        return 'OK', 200

    # --------------------------------------------------------------------------------------------
    # A callback function that is called by Bank API to notify about changes (corporate Account)
    # The json format is: {"event": "ach.update", "op": "update", "id": "ach_01123456789", "url": "blabla"}
    # --------------------------------------------------------------------------------------------
    def _bankapihook_corp(self):
        result = self._bankapihook_process_data()
        if not result:
            return 'Internal Server Error', 500
        return 'OK', 200

    # --------------------------------------------------------------------------
    # Process User deposits
    # --------------------------------------------------------------------------
    def _process_user_deposits(self):
        bankapi = BankAPI.get_instance()
        tran_list = bankapi.process_users_transactions()
        if tran_list is None:
            self.glogger.info("No actual transaction to process")
            return False
        self.glogger.info("The following transfers have been processed: %s", str(tran_list))

    # ----------------------------------------
    # Get all secrets from KV
    # ----------------------------------------
    def _getallkv(self):
        return self._doaction_on_kv_all("get_all_secrets", "getallkv")

    # ----------------------------------------
    # Delete all secrets from KV
    # ----------------------------------------
    def _delallkv(self):
        return self._doaction_on_kv_all("delete_all_secrets", "delallkv")

    # ----------------------------------------
    # Initialze the mandatory keys in the KV
    # ----------------------------------------
    def _initkv(self):
        return self._doaction_on_kv_all("init_mandatory_secrets", "initkv")

    # ------------------------------------------------------------------------------
    # Execute a function on q table
    # The function must expect for up to two parameters: idx (userid), and other
    # -----------------------------------------------------------------------------
    def __doaction_on_tables(self, tables_fetcher: str, func_name, resp_key_name, parm1=None, parm2=None):
        response = {}
        func_command = tables_fetcher + "." + func_name + "("
        if parm1:
            func_command = func_command + "\'" + parm1 + "\'"
        if parm2:
            func_command = func_command + ",\'" + parm2 + "\'"
        func_command = func_command + ")"
        try:
            result = eval(func_command)
        except Exception as err:
            self.glogger.error("Failed to run function: %s err=%s", func_command, err)
            self._add_item_to_response(response, resp_key_name, "Failed to Run: " + func_command)
            return response
        self._add_item_to_response(response, resp_key_name, result)
        if parm1:
            self._add_item_to_response(response, 'userid', parm1)
        if parm2:
            self._add_item_to_response(response, 'param2', parm2)
        return response

    # ----------------------------------------------------------------------
    # Execute a function on the users table - all Users
    # ----------------------------------------------------------------------
    def _doaction_on_usertables_all(self, func_name, resp_key_name):
        return self.__doaction_on_tables("self.dbhandles.get_usertables()", func_name, resp_key_name)

    # ----------------------------------------------------------------------
    # Execute a function on the users table - all Users - with single param
    # ----------------------------------------------------------------------
    def _doaction_on_usertables_all_single_param(self, func_name, resp_key_name, param1):
        return self.__doaction_on_tables("self.dbhandles.get_usertables()", func_name, resp_key_name, param1)

    # -----------------------------------------------------------------------------
    # Execute a function on the users table - with two params: param1 and param2
    # -----------------------------------------------------------------------------
    def _doaction_on_usertables_all_two_params(self, func_name, resp_key_name, param1, parm2):
        return self.__doaction_on_tables("self.dbhandles.get_usertables()", func_name, resp_key_name, param1, parm2)

    # ------------------------------------------------------------------------------
    # Execute a function on the users table (With single parameter: User ID)
    # -----------------------------------------------------------------------------
    def _doaction_on_usertables_single_idx(self, func_name, resp_key_name):
        response, userid = self._get_userid_param()
        if response:
            return response
        return self.__doaction_on_tables("self.dbhandles.get_usertables()", func_name, resp_key_name, userid)

    # -----------------------------------------------------------------------------
    # Execute a function on the users table - with two params: user ID and other
    # -----------------------------------------------------------------------------
    def _doaction_on_usertables_two_params(self, func_name, resp_key_name, parm2):
        response, userid = self._get_userid_param()
        if response:
            return response
        return self.__doaction_on_tables("self.dbhandles.get_usertables()", func_name, resp_key_name, userid, parm2)

    # ----------------------------------------------------------------------
    # Execute a function on the RIA table - all RIAs
    # ----------------------------------------------------------------------
    def _doaction_on_riatables_all(self, func_name, resp_key_name):
        return self.__doaction_on_tables("self.dbhandles.get_RIAtables()", func_name, resp_key_name)

    # ----------------------------------------------------------------------
    # Execute a function on the RIA table - all RIAs -  all Users - with single param
    # ----------------------------------------------------------------------
    def _doaction_on_riatables_all_single_param(self, func_name, resp_key_name, param1):
        return self.__doaction_on_tables("self.dbhandles.get_RIAtables()", func_name, resp_key_name, param1)

    # ------------------------------------------------------------------------------
    # Execute a function on the RIA table (With single parameter: User ID)
    # -----------------------------------------------------------------------------
    def _doaction_on_riatables_single_idx(self, func_name, resp_key_name):
        response, userid = self._get_userid_param()
        if response:
            return response
        return self.__doaction_on_tables("self.dbhandles.get_RIAtables()", func_name, resp_key_name, userid)

    # -----------------------------------------------------------------------------
    # Execute a function on the RIA table - with two params: user ID and other
    # -----------------------------------------------------------------------------
    def _doaction_on_riatables_two_params(self, func_name, resp_key_name, parm2):
        response, userid = self._get_userid_param()
        if response:
            return response
        return self.__doaction_on_tables("self.dbhandles.get_RIAtables()", func_name, resp_key_name, userid, parm2)

    # ----------------------------------------------------------------------
    # Execute a function on the Potential-Clients Table - all potential
    # ----------------------------------------------------------------------
    def _doaction_on_potentialtables_all_single_param(self, func_name, resp_key_name, param1):
        return self.__doaction_on_tables("self.dbhandles.get_potential_clients_tables()", func_name, resp_key_name,
                                         param1)

    # ----------------------------------------------------------------------
    # Execute a function on the Potential Customers table - all - with single param
    # ----------------------------------------------------------------------
    def _doaction_on_potentialtables_all_single_param(self, func_name, resp_key_name, param1):
        return self.__doaction_on_tables("self.dbhandles.get_potential_clients_tables()", func_name, resp_key_name,
                                         param1)

    # ------------------------------------------------------------------------------
    # Execute a function on the Potential-Clients Table (With single parameter: User ID)
    # -----------------------------------------------------------------------------
    def _doaction_on_potentialtables_single_idx(self, func_name, resp_key_name):
        response, userid = self._get_userid_param()
        if response:
            return response
        return self.__doaction_on_tables("self.dbhandles.get_potential_clients_tables()", func_name, resp_key_name,
                                         userid)

    # -----------------------------------------------------------------------------
    # Execute a function on the Potential-Clients Table - with two params: user ID and other
    # -----------------------------------------------------------------------------
    def _doaction_on_potentialtables_two_params(self, func_name, resp_key_name, parm2):
        response, userid = self._get_userid_param()
        if response:
            return response
        return self.__doaction_on_tables("self.dbhandles.get_potential_clients_tables()", func_name, resp_key_name,
                                         userid, parm2)

    # ----------------------------------------------------------------------
    # Execute a function on the Keyvalut
    # ----------------------------------------------------------------------
    def _doaction_on_kv_all(self, func_name, resp_key_name):
        return self.__doaction_on_tables("AzureKeyVaultWrapper.get_instance()", func_name, resp_key_name)

    # ----------------------------------------------------------------------
    # Execute a function on the Files table - all Records/Files
    # ----------------------------------------------------------------------
    def _doaction_on_filetables_all(self, func_name, resp_key_name):
        return self.__doaction_on_tables("self.dbhandles.get_filetables()", func_name, resp_key_name)

    # ----------------------------------------------------------------------
    # Execute a function on the Files table - all Files - with single param
    # ----------------------------------------------------------------------
    def _doaction_on_filetables_all_single_param(self, func_name, resp_key_name, param1):
        return self.__doaction_on_tables("self.dbhandles.get_filetables()", func_name, resp_key_name, param1)

    # ----------------------------------------
    # Update the data of a user
    # ----------------------------------------
    def _updateuserdata(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        response, table = self._get_table_param()
        if response:
            return response
        response, data_dict = self._get_data_dict_param()
        if response:
            return response
        response = {}
        self.dbhandles.get_usertables().update_values(userid, table, data_dict)
        self._add_item_to_response(response, 'updateuserdata', data_dict)
        return response

    # ----------------------------------------
    # Update the data of a RIA table
    # ----------------------------------------
    # def _updateriadata(self):
    #    response, userid = self._get_userid_param()
    #    if response:
    #        return response
    #    table = self.dbhandles.get_RIAtables().tab_name_data
    #    response, data_dict = self._get_data_dict_param()
    #    if response:
    #        return response
    #    response = {}
    #    self.dbhandles.get_usertables().update_values(userid, table, data_dict)
    #    self._add_item_to_response(response, 'updateriadata', data_dict)
    #    return response

    # ----------------------------------------
    # Update the data of a daily table
    # ----------------------------------------
    def _updatedailydata(self):
        response, date = self._get_param('date')
        if response:
            return response
        table = self.dbhandles.get_dailydatatable().tab_name_daily
        response, data_dict = self._get_data_dict_param()
        if response:
            return response
        response = {}
        self.dbhandles.get_usertables().update_values(date, table, data_dict)
        self._add_item_to_response(response, 'updatedailydata', data_dict)
        return response

    # ----------------------------------------
    # Update the data of a user table (not pii)
    # ----------------------------------------
    def _updateuserdata2(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        table = self.dbhandles.get_usertables().tab_name_data
        response, data_dict = self._get_data_dict_param()
        if response:
            return response
        response = {}
        self.dbhandles.get_usertables().update_values(userid, table, data_dict)
        self._add_item_to_response(response, 'updateuserdata2', data_dict)
        return response

    # ----------------------------------------
    # Execution an action by function name
    # ----------------------------------------
    def _doaction(self):
        response, func = self._get_param('func')
        if response:
            return response
        response, param = self._get_param('param')
        if response:
            return response
        response = {}
        try:
            if param == "None":
                result = eval(func + "()")
            else:
                result = eval(func + "(" + param + ")")
        except Exception as err:
            self.glogger.error("Failed to run function: %s with param: %s. err=%s", func, param, err)
            self._add_item_to_response(response, 'actresult', "Failed to Run: " + func + " " + param)
            return response
        self.glogger.info("%s(%s) exectuted. result=%s", func, param, result)
        self._add_item_to_response(response, 'actresult', "Completed function call: " + func + "(" + param + ")")
        self._add_item_to_response(response, 'funcresult', result)
        return response

    # -------------------------------------------------------
    # List the files in the home directory
    # Example from here: https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html
    # -------------------------------------------------------
    def _listfsfiles(self):
        response = {}
        #file_list = fileop_list_fs_files()
        uploaded_list_file = FsFiles().list_uploaded_files()
        downloaded_list_file = FsFiles().list_downloaded_files()
        self._add_item_to_response(response, 'uploaded', uploaded_list_file)
        self._add_item_to_response(response, 'downloaded', downloaded_list_file)
        return response

    # -------------------------------------------------------
    # Delete files in the home directory
    # -------------------------------------------------------
    def _deletefsfile(self):
        response, file_ext = self._get_param("ext")
        if response:
            return response
        response = {}
        uploaded_list_file = delete_uploaded_files(file_ext)
        downloaded_list_file = delete_downloaded_files(file_ext)
        self._add_item_to_response(response, 'uploaded', uploaded_list_file)
        self._add_item_to_response(response, 'downloaded', downloaded_list_file)
        return response

    # -------------------------------------------------------
    # Download a file from File System
    # -------------------------------------------------------
    def _downloadfsfile(self):
        response, file_name = self._get_param("file")
        if response:
            return response
        result = FsFiles().download_file_from_download_folder(file_name)
        #result = fileop_download_fs_file(file_name)
        if result is None:
            response = {}
            self._add_item_to_response(response, 'downloadfsfile', "File not found to download or I/O error")
            return response
        return result # Stream

    # -------------------------------------------------------
    # Download the log file
    # -------------------------------------------------------
    def _downloadlogfile(self):
        self.glogger.debug("Downloading Log File...")
        response = {}
        result = FsFiles().download_logfile()
        #result = fileop_download_logfile()
        if result is None:
            response = {}
            self._add_item_to_response(response, 'downloadlogfile', "Log file not found to download or I/O error")
            return response
        return result  # Streaming - be careful: do not return dictionary

    # -------------------------------------------------------
    # Upload the log file to the storage
    # -------------------------------------------------------
    def _uploadlogfile(self):
        self.glogger.debug("Uploading the Log File to the Azure Storage...")
        response = {}
        result = LogFilesStorage().upload_current_log_file()
        if result is None:
            response = {}
            self._add_item_to_response(response, 'uploadlogfile', "Log file not found to upload or I/O error")
            return response
        self._add_item_to_response(response, 'uploadlogfile', result)
        return response

    # -------------------------------------------------------
    # Upload a file to the FileSystem on the server server
    # Example from here: https://github.com/ahmedfgad/AndroidFlask/blob/master/Part%201/FlaskServer/flask_server.py
    # Example from here: https://stackoverflow.com/questions/56766072/post-method-to-upload-file-with-json-object-in-python-flask-app
    # -------------------------------------------------------
    def _uploadfile2fs(self):
      #response, file_list = self._get_filelist_param()
      #if response:
      #    return response
       response = {}
       fname_list = FsFiles().upload_files()
       #fname_list = fileop_upload_files_2fs(file_list)
       if fname_list is None:
           self._add_item_to_response(response, 'uploadfile2fs', "Failed to upload file (to fs) or I/O error")
           return response
       self._add_item_to_response(response, 'uploadfile2fs', file_list)
       return response

    # ------------------------------------------------------------------------------------------------------
    # Upload an contract to the database and to the storage
    # ------------------------------------------------------------------------------------------------------
    def _uploadcontract(self):
        response = {}
        result = ContractStorage().upload()
        self._add_item_to_response(response, 'uploadcontract', result)
        return response
        #userid = auth_get_current_userid()
        #response, file_list = self._get_filelist_param()
        #if response:
        #    return response
        #response = {}
        #filename = fileop_upload_files_2db(self.dbhandles.get_filetables(), userid, file_list)
        #if filename is None:
        #    self.glogger.error("Failed to upload file to the database")
        #    self._add_item_to_response(response, 'uploadfile2db', "Failed to upload file (to db) or I/O error")
        #    return response
        #self._add_item_to_response(response, 'uploadfile2db', filename)
        #return response


    # ----------------------------------------
    # Show the list of the files stored in the database
    # ----------------------------------------
    def _listdbfiles(self):
        return self._doaction_on_filetables_all("get_all_files_info", "listdbfiles")

    # ----------------------------------------
    # Delete a file from the database
    # ----------------------------------------
    def _deletedbfile(self):
        response, fname = self._get_param("file")
        if response:
            return response
        return self._doaction_on_filetables_all_single_param("delete_record", "listdbfiles", fname)

    # ------------------------------------------------------------------------------------------------------
    # Download the image of a specific user
    # ------------------------------------------------------------------------------------------------------
    # def __downloadimage(self, userid: str):
    #    self.glogger.info("Downloading user %s image", userid)
    #    result = fileop_download_user_image(self._fetch_userpii_object(), userid)
    #    if result is None:
    #        response = {}
    #        self._add_item_to_response(response, 'downloadimage', "Image file not found to download or I/O error")
    #        return response
    #    return result  # Streaming - be careful: do not return dictionary

    # ------------------------------------------------------------------------------------------------------
    # Download the image of a specific user
    # ------------------------------------------------------------------------------------------------------
    # def _downloadimage(self):
    #    userid = auth_get_current_userid()
    #    return self.__downloadimage(userid)
    #
    # ------------------------------------------------------------------------------------------------------
    # Download the image of a user
    # ------------------------------------------------------------------------------------------------------
    # def _userimage(self):
    #    response, userid = self._get_userid_param()
    #    if response:
    #        return response
    #    return self.__downloadimage(userid)

    # ------------------------------------------------------------------------------------------------------
    # Delete the image of the user (profile)
    # ------------------------------------------------------------------------------------------------------
    # def _deleteimage(self):
    #    return self._setdefaultimage()
    #
    # ------------------------------------------------------------------------------------------------------
    # Set default image to the user
    # ------------------------------------------------------------------------------------------------------
    # def _setdefaultimage(self):
    #    response, userid = self._get_userid_param()
    #    if response:
    #        return response
    #    response = {}
    #    self.glogger.info("Setting default image to the user: %s", userid)
    #    fname = fileop_set_default_image(self._fetch_userpii_object(), userid)
    #    self._add_item_to_response(response, 'defaultimage', fname)
    #    return response

    # ------------------------------------------------------------------------------------------------------
    # Get the list of the images size
    # ------------------------------------------------------------------------------------------------------
    # def _imagessize(self):
    #    response = {}
    #    self.glogger.info("Getting the list of the size of the images")
    #    image_list = image_get_picture_list(self._fetch_userpii_object())
    #    self._add_item_to_response(response, 'imagessize', image_list)
    #    return response

    # ------------------------------------------------------------------------------------------------------
    # Get the schema of the database
    # ------------------------------------------------------------------------------------------------------
    # def _schema(self):
    #    response = {}
    #    self.glogger.info("Getting the Schema of the database")
    #    schmaobj = self._fetch_schema_object()
    #    schema = schmaobj.get_all_column_names()
    #    self._add_item_to_response(response, 'schema', schema)
    #    return response
    #
    # ------------------------------------------------------------------------------------------------------
    # Get the schema Scopes
    # ------------------------------------------------------------------------------------------------------
    # def _schemascope(self):
    #    response = {}
    #    self.glogger.info("Getting the Schema Scopes")
    #    schmaobj = self._fetch_schema_object()
    #    scopes = schmaobj.get_all_scopes()
    #    self._add_item_to_response(response, 'scope', scopes)
    #    return response

    # ------------------------------------------------------------------------------------------------------
    # Create handles (accounts) for the user
    # ------------------------------------------------------------------------------------------------------
    # def _createuserhandle(self):
    #    response, userid = self._get_userid_param()
    #    if response:
    #        return response
    #    response, userhandle = self._get_userhandle_param()
    #    if response:
    #        return response
    #    response = {}
    #    userhandleaobj = self._fetch_userhandle_object()
    #    userhandleaobj.add_private_handle(userid, userhandle) # first add the userhandle if it does not exist
    #    handles = userhandleaobj.create_temporary_handles(userid)
    #    self._add_item_to_response(response, 'userhandles', handles)
    #    return response

    # ------------------------------------------------------------------------------------------------------
    # An invalid function/url was called
    # ------------------------------------------------------------------------------------------------------
    def _invalidurl(self):
        return None  # This will set the result as Fail

    # ------------------------------------------------------------------------------------------------------
    # Get a User Object - If exists in the flask, use it, otherwise Create it
    # ------------------------------------------------------------------------------------------------------
    # def _fetch_userpii_object(self):
    #    return self.dbhandles.get_userpii()

    # ------------------------------------------------------------------------------------------------------
    # Get a UserTables Object - If exists , use it, otherwise Create it
    # ------------------------------------------------------------------------------------------------------
    # def _fetch_usertables_object(self):
    #    return self.dbhandles.get_usertables()

    # ------------------------------------------------------------------------------------------------------
    # Get a Schema Object - If exists in the flask, use it, otherwise Create it
    # ------------------------------------------------------------------------------------------------------
    # def _fetch_schema_object(self):
    #    schemaobj = schema_get_object()
    #    return schemaobj

    # ------------------------------------------------------------------------------------------------------
    # Get a UserHandle Object - If exists in the flask, use it, otherwise Create it
    # ------------------------------------------------------------------------------------------------------
    # def _fetch_userhandle_object(self):
    #    userhandleaobj = userhandle_get_object()
    #    return userhandleaobj

    # ---------------------------------
    # Return Version
    # ---------------------------------
    def _get_version(self):
        if utils_is_dev_env():
            version = self._version + "D"
        else:
            version = self._version + "P"
        return version

    # -----------------------------------
    # Get User Info
    # -----------------------------------
    def _getuserinfo(self, response: dict, logged_user_id=None):
        # self._add_item_to_response(response, 'isnew', session_is_new_user())
        self._add_item_to_response(response, 'logged', session_is_logged_in())
        self._add_item_to_response(response, 'session', session_get_user_info())
        # self._add_item_to_response(response, 'access_token', session_get_access_token())
        # self._add_item_to_response(response, 'refresh_token', session_get_refresh_token())
        self._add_item_to_response(response, 'Name', session_get_user_first_name())
        self._add_item_to_response(response, 'Last', session_get_user_last_name())
        self._add_item_to_response(response, 'eMail', session_get_user_email())
        # self._add_item_to_response(response, 'Country', session_get_user_country())
        self._add_item_to_response(response, 'State', session_get_user_state())
        # self._add_item_to_response(response, 'City', session_get_user_city())
        # self._add_item_to_response(response, 'Street', session_get_user_street())
        # self._add_item_to_response(response, 'PostalCode', session_get_user_postalcode())
        # self._add_item_to_response(response, 'AsAdmin', session_get_auth_mode_as_admin())
        self._add_item_to_response(response, 'Phone', session_get_user_phone_number())
        self._add_item_to_response(response, 'IndCRD', session_get_user_crd_number())
        self._add_item_to_response(response, 'FirmCRD', session_get_company_crd_number())
        self._add_item_to_response(response, 'Company', session_get_company_name())
        # self._add_item_to_response(response, 'JobTitle', session_get_user_jobtitle())
        self._add_item_to_response(response, 'ParentID', self.dbhandles.get_usertables().get_parentid(logged_user_id))
        self._add_item_to_response(response, 'UserType', session_get_user_type())

    ########################### RIA API ########################################################################

    # ----------------------------------------
    # Add an advisor
    # ----------------------------------------
    def _addnewadvisor(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        response, crd_individual = self._get_param('crdindividual')
        if response:
            return response
        response, crd_firm = self._get_param('crdfirm')
        if response:
            return response

        response, associated = self._get_param('associated')
        if response:
            return response
        response, advisor_info = self._get_dict_param('advisorinfo')
        if response:
            return response

        result = self.dbhandles.get_RIAtables().add_new_advisor(idx=userid,
                                                                crd_individual=crd_individual, crd_firm=crd_individual,
                                                                associated=associated, advisor_info=advisor_info)
        response = {}
        self._add_item_to_response(response, 'addnewadvisor', str(userid))
        self._add_item_to_response(response, 'result', str(result))
        return response

    # ----------------------------------------
    # list advisors for associated RIA
    # ----------------------------------------
    # todo:
    # add option to get all RIA's (with any associated)
    def _getallassociatedrias(self):
        # response, userid = self._get_userid_param()
        # if response:
        #     return response
        response, associated = self._get_param('associated')
        if response:
            return response
        RIAs = self.dbhandles.get_RIAtables().get_all_associated_RIAs(associated)
        response = {}
        self._add_item_to_response(response, 'getallassociatedrias', RIAs)
        return response

    # ----------------------------------------
    # is_advisor (userid)
    # ----------------------------------------
    def _isadvisor(self):
        return self._doaction_on_riatables_single_idx("is_advisor", "isadvisor")

    # response, userid = self._get_userid_param()
    # if response:
    #    return response
    # is_adv = self.dbhandles.get_RIAtables().is_advisor(userid)
    # response = {}
    # self._add_item_to_response(response, 'isadvisor', is_adv)
    # return response

    # ----------------------------------------
    # get_RIA_info (userid)
    # ----------------------------------------
    def _getadvisorinfo(self):
        return self._doaction_on_riatables_single_idx("get_advisor_info", "advisor_info")
        # response, userid = self._get_userid_param()
        # if response:
        #    return response
        # ret = self.dbhandles.get_RIAtables().get_advisor_info(userid)
        # response = {}
        # self._add_item_to_response(response, 'get_advisor_info', ret)
        # return response

    # ----------------------------------------
    # addchild (advisorid, userid)
    # ----------------------------------------
    def _addchild(self):
        response, advisor_id = self._get_param('advisorid')
        if response:
            return response
        return self._doaction_on_riatables_two_params("add_child", "addchild", advisor_id)
        # response, userid = self._get_param('userid')
        # if response:
        #    return response

    #
    # ret = self.dbhandles.get_RIAtables().add_child(advisor_id, userid)
    # response = {}
    # self._add_item_to_response(response, 'addchild', ret)
    # return response

    # ----------------------------------------
    # delchild (userid) - set's client's parent to null
    # discuss with Danny do we need here RIA id?
    # ----------------------------------------
    def _delchild(self):
        return self._doaction_on_riatables_single_idx("del_child", "delchild")
        # response, userid = self._get_userid_param()
        # if response:
        #    return response

    #
    # ret = self.dbhandles.get_RIAtables().del_child(userid)
    # response = {}
    # self._add_item_to_response(response, 'delchild', ret)
    # return response

    # ----------------------------------------
    # get_advisor_children (idx)
    # ----------------------------------------
    def _getadvisorchildren(self):
        return self._doaction_on_riatables_single_idx("get_advisor_children", "getadvisorchildren")
        # response, userid = self._get_userid_param()
        # if response:
        #    return response

    #
    # ret = self.dbhandles.get_RIAtables().get_advisor_children(userid)
    # response = {}
    # self._add_item_to_response(response, 'getadvisorchildren', ret)
    # return response

    # ----------------------------------------
    # _getadvisorchildrenstatus (userid, status)
    # ----------------------------------------
    def _getadvisorchildrenstatus(self):
        response, status = self._get_param('status')
        if response:
            return response
        return self._doaction_on_riatables_two_params("_get_all_specific_statusflag", "getadvisorchildrenstatus",
                                                      status)
        # response, userid = self._get_userid_param()
        # if response:
        #    return response
        # response, status = self._get_param('status')
        # if response:
        #    return response
        # ret = self.dbhandles.get_RIAtables()._get_all_specific_statusflag(userid, status)
        # response = {}
        # self._add_item_to_response(response, 'getadvisorchildrenstatus', ret)
        # return response

    # ----------------------------------------
    # Get change feeds of the advisor tables
    # ----------------------------------------
    def _advisorschangefeed(self):
        response, start_date_time = self._get_param('start')
        if response:
            return response
        return self._doaction_on_riatables_all_single_param('get_all_change_feeds', 'advisorschangefeed',
                                                            start_date_time)

    # ----------------------------------------
    # Get the list of the registerd admins
    # ----------------------------------------
    def _getadmins(self):
        response = {}
        admins = UserType.get_instance().get_admins()
        self._add_item_to_response(response, 'admins', admins)
        return response

    # --------------------------------------------------
    # add an admin to the list of the registered admins
    # --------------------------------------------------
    def _addadmin(self):
        response, admin = self._get_param('admin')
        if response:
            return response
        response = {}
        result = UserType.get_instance().add_admin(admin)
        self._add_item_to_response(response, 'addadmin', result)
        return response

    # --------------------------------------------------
    # Delete an admin from the list of the registered admins
    # --------------------------------------------------
    def _deladmin(self):
        response, admin = self._get_param('admin')
        if response:
            return response
        response = {}
        result = UserType.get_instance().del_admin(admin)
        self._add_item_to_response(response, 'deladmin', result)
        return response

    # --------------------------------------------------
    # Dedeuct Fee
    # --------------------------------------------------
    def __deductfee(self, fee_type: str):
        response, userid = self._get_userid_param()
        if response:
            return response
        response, amount = self._get_amount_param()
        if response:
            return response
        response, sharecost = self._get_sharecost_param()
        if response:
            return response
        fee = Fee()
        if fee_type == 'mng':
            result = fee.deduct_management_fee(userid, amount, sharecost)
        if fee_type == 'sign':
            result = fee.deduct_signup_fee(userid, amount, sharecost)
        if fee_type == 'misc':
            result = fee.deduct_misc_fee(userid, amount, sharecost)
        response = {}
        self._add_item_to_response(response, 'deductfee', result)
        return response

    # --------------------------------------------------
    # Dedeuct Fee
    # --------------------------------------------------
    def _deductmngfee(self):
        return self.__deductfee('mng')

    def _deductsignfee(self):
        return self.__deductfee('sign')

    def _deductmiscfee(self):
        return self.__deductfee('misc')

    # ----------------------------------------
    # Get user transactions
    # ----------------------------------------
    def _transactions(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        trtable = self.dbhandles.get_transactiontable()
        transactions = trtable.get_all_values(userid)
        response = {}
        self._add_item_to_response(response, 'transactions', transactions)
        return response

    # ----------------------------------------
    # Get user balance
    # ----------------------------------------
    def _userbalance(self):
        response, userid = self._get_userid_param()
        if response:
            return response
        trtable = self.dbhandles.get_transactiontable()
        user_amounts = trtable.get_user_values(userid)
        user_total = trtable.get_total_user_amounts(userid)
        user_shares = trtable.get_total_user_shares(userid)
        balance = {"amount": user_amounts, "total": user_total, "shares": user_shares}
        response = {}
        self._add_item_to_response(response, 'balance', balance)
        return response

    # ------------------------------------------------------------------
    # Checks if an email already exists in the active directory
    # ------------------------------------------------------------------
    def _emailexists(self):
        response, email = self._get_param('email')
        if response:
            return response
        userid = MsGraphApp().get_id_by_email(email)
        response = {}
        if userid is None:
            self._add_item_to_response(response, 'exists', False)
        else:
            self._add_item_to_response(response, 'exists', True)
            if config_is_dev_mode():
                self._add_item_to_response(response, 'userid', userid)
        return response

    # ----------------------------------------
    # Get Users list (from Active Directory)
    # ----------------------------------------
    def _getusersinfo(self):
        # usersinfo = AzureADWrapper.get_instance().get_all_users_info()
        # usersinfo, retcode = MsGraphApp.get_instance().get_users_list()
        usersinfo = MsGraphApp().get_users_list()
        if usersinfo is None:
            self.glogger.error("No User found in the Active Directory !!!!")
        response = {}
        self._add_item_to_response(response, 'getusersinfo', usersinfo)
        return response

    # ----------------------------------------
    # Get Users Emails (from Active Directory)
    # ----------------------------------------
    def _getusersemail(self):
        # usersinfo, retcode = MsGraphApp.get_instance().get_all_users_email()
        usersinfo = MsGraphApp().get_all_users_email()
        if usersinfo is None:
            self.glogger.error("No User found in the Active Directory !!!!")
        response = {}
        self._add_item_to_response(response, 'getusersemail', usersinfo)
        return response

    # ----------------------------------------
    # Get a user in the Active Directory
    # ----------------------------------------
    def _createuser(self):
        response, firstname = self._get_param('firstname')
        if response:
            return response
        response, lastname = self._get_param('lastname')
        if response:
            return response
        response, email = self._get_param('email')
        if response:
            return response
        response, street = self._get_param('street')
        if response:
            return response
        response, city = self._get_param('city')
        if response:
            return response
        response, zip = self._get_param('zip')
        if response:
            return response
        # usersinfo, retcode = MsGraphApp.get_instance().create_new_user(firstname, lastname, email)
        usersinfo = MsGraphApp().create_new_user(firstname, lastname, email)
        if usersinfo is None:
            self.glogger.error("failed to create a user (%s %s %s %s %s %s)", firstname, lastname, email, street, city,
                               zip)
            response = {}
            self._add_item_to_response(response, 'createuser', usersinfo)
            return response
        idx = usersinfo["id"]
        # usersinfo, retcode = MsGraphApp.get_instance().update_user_address(idx, street, city, zip)
        usersinfo = MsGraphApp().update_user_address(idx, street, city, zip)
        if usersinfo is None:
            self.glogger.error("failed to add user address to AAD (%s %s %s %s %s %s)", firstname, lastname, email,
                               street, city, zip)
            response = {}
            self._add_item_to_response(response, 'createuser', usersinfo)
            return response
        response = {}
        self._add_item_to_response(response, 'createuser', usersinfo)
        return response

    # ------------------------------------------------
    # Get user signed contracts
    # ------------------------------------------------
    def _getusercontracts(self):
        response, user_idx = self._get_param('userid')
        if response:
            return False
        return self._doaction_on_usertables_all_single_param('user_contracts', 'getuserscontracts',
                                                             user_idx)

    # ------------------------------------------------
    # add a signed contract to a user
    # ------------------------------------------------
    def _addusercontract(self):
        response, user_idx = self._get_param('userid')
        if response:
            return False

        response, new_contract = self._get_dict_param('contract')
        if response:
            return False

        # return self._doaction_on_usertables_all_two_params('user_contracts', 'adduserscontract',
        #                                                    user_idx, str(new_contract))

        res = self.dbhandles.get_usertables().user_contracts(idx=user_idx, new_contract=new_contract)

        response = {}
        self._add_item_to_response(response, "contracts", res)
        return response


    # ------------------------------------------------
    # Calculate the payout for a set of parameters
    # ------------------------------------------------
    def _simulate_prospect(self):
        response, gender = self._get_param('gender')
        if response:
            return response
        gender = gender.upper()
        response, current_age = self._get_int_param('current_age')
        if response:
            return response
        response, average_return = self._get_float_param('average_return')
        if response:
            return response
        response, funding_amount = self._get_float_param('funding_amount')
        if response:
            return response
        response, payout_age = self._get_int_param('payout_age')
        if response:
            return response
        response = {}
        if not gender.startswith('M') and not gender.startswith('F'):
            self.glogger.error("Gender must be either F or M")
            self._add_item_to_response(response, 'simulate', 'Invalid Gender')
            return response
        if current_age > 90:
            self.glogger.error("Age must be <= 90")
            self._add_item_to_response(response, 'simulate', 'Invalid Age')
            return response
        age_list = self.__get_payout_age_list(payout_age)
        output = {}
        for age in age_list:
            rec = {}
            with_savvly, without_savvly, multiplier = \
                calculate_payout(gender, current_age, average_return, funding_amount, age)
            with_savvly = int(round(with_savvly, 0))
            without_savvly = int(round(without_savvly, 0))
            multiplier = format(multiplier, ".2f")
            rec["gender"] = gender
            rec["current_age"] = current_age
            rec["average_return"] = int(average_return)
            rec["funding_amount"] = int(funding_amount)
            rec["payout_age"] = payout_age
            # rec["gender"] = age
            rec["withRounded"] = with_savvly
            rec["withoutRounded"] = without_savvly
            rec["multiplierRound"] = multiplier
            output[str(age)] = rec
        response = {}
        self._add_item_to_response(response, 'simulate', output)
        return response

    # ---------------------------------------------------------------
    # Get the list of the ages starting from a specified age
    # ---------------------------------------------------------------
    def __get_payout_age_list(self, start_age) -> list:
        age_list = [start_age, 80, 85, 90]
        # for inx in range(3):
        #    age = start_age + (inx * 5)
        #    if age >= 90:
        #        break
        #    age_list.append(age)
        return age_list

        # ---------------------------------------------------------------

    # Get and Store User Type
    # ---------------------------------------------------------------
    def _get_store_user_type(self, logged_user_id):
        try:
            user_type = UserType.get_instance().get_user_type(
                logged_user_id)  # Find the user type and store in the session
            if user_type is not None:
                session_set_user_type(user_type)
                return user_type
        except Exception as err:
            self.glogger.error("Failed to get User Type. err=%s", err)
        return None

    # ---------------------------------------------------------------
    # Process logged user: Check if new nd process, get its type
    # ---------------------------------------------------------------
    def _process_logged_in_user(self, logged_user_id):
        user_type = self._get_store_user_type(logged_user_id)
        if user_type is not None:
            return True  # This user is already known - not new

        try:
            crd_individual = session_get_user_crd_number()
            crd_firm = session_get_company_crd_number()
            associated = session_get_company_name()
            self.glogger.info("id=%s crd_ind=%s crd_firm=%s firm=%s", logged_user_id, crd_individual, crd_firm,
                              associated)
            if crd_individual is None and crd_firm is None:
                self.glogger.info("Adding a new user. id=%s", logged_user_id)
                userinfo = {}
                result = self.dbhandles.get_usertables().add_new_user(logged_user_id, userinfo)
                session_set_user_type_as_client()
                return result
            else:
                self.glogger.info("Adding a new Advisor. id=%s crd_ind=%s crd_firm=%s firm=%s", logged_user_id,
                                  crd_individual, crd_firm, associated)
                advisor_info = {}
                advisor_info["firstname"] = session_get_user_first_name()
                advisor_info["lastname"] = session_get_user_last_name()
                advisor_info["address"] = session_get_user_state()
                advisor_info["email"] = session_get_user_email()
                advisor_info["phone"] = session_get_user_phone_number()
                result = self.dbhandles.get_RIAtables().add_new_advisor(idx=logged_user_id,
                                                                        crd_individual=crd_individual,
                                                                        crd_firm=crd_firm,
                                                                        associated=associated,
                                                                        advisor_info=advisor_info)
                session_set_user_type_as_advisor()  # Not-validated: First, assume the advisor is not validated
                session_set_user_type_as_validated_advisor()  # @todo remove this
                if not result:
                    self.glogger.error("Failed to add an advisor (%s) to the DB. result=%s", logged_user_id, result)
                    return result
        except Exception as err:
            self.glogger.error("Failed to add new User to the database. err=%s", err)
            return False
        try:
            NewUser().process(logged_user_id)  # If this is a new user, handle it
        except Exception as err:
            self.glogger.error("Failed to process the new user. err=%s", err)
            return False
        return True

    # -----------------------------------
    # Set Response Headers
    # -----------------------------------
    # def set_response_header(self, response):
    # return response
    # resp.headers.add('Set-Cookie', f'session=%s; SameSite=None; Secure' % request_get_cookies())
    # resp.headers.add("Access-Control-Allow-Origin", "*");
    # resp.headers.add("Access-Control-Max-Age", "1440");
    # resp.headers.add("Access-Control-Allow-Origin", "http://localhost:5000");
    # resp.headers.add("Access-Control-Allow-Headers", "Authorization, Origin, X-Requested-With, Content-Type, Accept");
    # white_origin = ['https://savvly-dev-api.azurewebsites.net',
    #                'http://localhost:5000',
    #                'https://savvlyb2c.b2clogin.com',
    #                'http://localhost:8080']
    # if request.referrer:
    #    self.glogger.info("request.referrer is: %s", request.referrer)
    #    host = request.referrer[:-1]
    # else:
    #    self.glogger.error("request.referrer is None. Cannot add headers")
    #    #print(request)
    #    host = white_origin[0]


# ---------------------------------------------------------------------------
# Set Response headers
# ---------------------------------------------------------------------------
# def proxy_set_response_header(response):   return Proxy.get_instance().set_response_header(response)


# ---------------------------------------------------------------------------
# Proxy function - Run an API
# ---------------------------------------------------------------------------
def proxy_run(func_name: str):   return Proxy.get_instance().run(func_name)

# ---------------------------------------------------------------------------
# Proxy function - Invalid API name passed - Create a response
# ---------------------------------------------------------------------------
# def proxy_invalid_api(func_name: str):
#    return Proxy.get_instance().invalid_api(func_name)
