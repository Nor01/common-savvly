import ast
from common.controllers.dbhandles import Dbhandles
from proxy.session import *
from common.kv.kv_wrapper import AzureKeyVaultWrapper
from common.util.config_wrapper import *


class UserType:
    __instance = None

    # ---------------------------------------------
    # Return the singletone object
    # ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if UserType.__instance is None:
            UserType()
        return UserType.__instance

    # ---------------------------------------------
    # Cconstructor
    # ---------------------------------------------
    def __init__(self):
        if UserType.__instance is not None:
            raise Exception("This class is a singleton!")
            return
        self.glogger = get_logger("UserType")
        UserType.__instance = self
        self.dbhandles = Dbhandles.get_instance()  # Get the instance of the dbhandles
        #self._admins = AzureKeyVaultWrapper.get_instance().get_secret("admins")
        self._admins = None

    # ---------------------------------------------
    # Get Admins list
    # ---------------------------------------------
    def _get_admins_list(self):
        admins = AzureKeyVaultWrapper.get_instance().get_secret("admins")
        if admins is None:
            self.glogger.error("Failed to get the list of the Admins from the KV")
            return None
        try:
            admins_list = ast.literal_eval(admins)
            self.glogger.debug("There are %d admins in the KV (type=%s)", len(admins_list), type(admins_list))
            return admins_list
        except Exception as err:
            self.glogger.error("Could not convert the Admins %s to List err=%s", admins, err)
            return None

    # ---------------------------------------------
    # Store Admins list
    # ---------------------------------------------
    def _store_admins_list(self, admins_list : list):
        AzureKeyVaultWrapper.get_instance().add_secret("admins", str(admins_list))
        self.get_admins()

    # ---------------------------------------------
    # Is this a normal user/client?
    # ---------------------------------------------
    def _is_user(self, userid):
        try:
            if userid is None:
                self.glogger.error("No user is logged in. Cannot determine if it is a Client")
                return False
            accountid = self.dbhandles.get_usertables().get_accountid(userid)
            if accountid is None:
                self.glogger.info("The user %s has no account in the database. Cannot determine if he is a client", userid)
                return False
            return True
        except Exception as err:
            self.glogger.error("Failed to check if this is a user (%s). Apparently the DB is empty", userid)
            return False

    # ---------------------------------------------
    # Is this an RIA/Advisor?
    # ---------------------------------------------
    def _is_advisor(self, userid):
        try:
            if userid is None:
                self.glogger.error("No user is logged in. Cannot determine if it is an RIA")
                return False
            is_advisor, is_validated = self.dbhandles.get_RIAtables().is_advisor(userid)
            self.glogger.info("Checked if advisor. Retured: %s %s", str(is_advisor), str(is_validated))
            return is_advisor, is_validated
        except Exception as err:
            self.glogger.error("Failed to check if this is an RIA (%s). Apparently the DB is empty", userid)
            return False, False

    # ---------------------------------------------
    # Is this a registered admin?
    # ---------------------------------------------
    def _is_admin(self, userid):
        try:
            if userid is None:
                self.glogger.error("No user is logged in. Cannot determine if it is an Admin")
                return False
            admin_list = self.get_admins()
            if admin_list is None:
                self.glogger.error("The admin list is None. Cannot check if %s is admin", userid)
                return False
            if userid in admin_list:
                self.glogger.info("The user=%s found in the admin", userid)
                return True
            self.glogger.debug("The user=%s is NOT an Admin", userid)
            return False
        except Exception as err:
            self.glogger.error("Failed to check if this is a admin (%s). Apparently the DB is empty", userid)
            return False

    # ---------------------------------------------
    # Get the user type: "user", "admin", "ria"
    # ---------------------------------------------
    def get_user_type(self, userid):
        if self._is_user(userid):
            self.glogger.info("This is a regular Client: %s.", userid)
            return "savvlyclient"
        is_advisor, is_validated = self._is_advisor(userid)
        if is_advisor and is_validated:
            self.glogger.info("This is a validated advisor: %s.", userid)
            return "savvlyvalidatedadvisor"
        if is_advisor and not is_validated:
            self.glogger.info("This is a not-validated advisor: %s.", userid)
            return "savvlyadvisor"
        if self._is_admin(userid):
            self.glogger.info("This is an Admin: %s.", userid)
            return "savvlyadmin"
        return None

        #--------------------------------------------------------------------------
        # This is a backdoor: If the ID is not in the system (DB & KV), use the
        # configuration parameters to behave as 'root' (admin)
        #--------------------------------------------------------------------------
        self.glogger.info("The id=%s found neither in the database nor in the KV.", userid)
        if config_is_dev_mode() and config_is_debug_mode() and config_is_admin_mode():
            self.glogger.info("In DEV/DEBUG/ADMIN configuration, behave as admin:%s", userid)
            return "savvlyadmin"
        self.glogger.error("The userid %s is not admin/ria/user", userid)
        return None

    # ---------------------------------------------
    # Add an admin to the registered list
    # ---------------------------------------------
    def add_admin(self, admin_id: str):
        admin_list = self.get_admins()
        if admin_list is None:
            self.glogger.error("The admin list is None. Cannot add admin: %s", admin_id)
            admin_list = []
        if admin_id in admin_list:
            self.glogger.error("The admin %s already exists in the admin list", admin_id)
            return False
        admin_list.append(admin_id)
        self._store_admins_list(admin_list)
        return True

    # ---------------------------------------------
    # Delete an admin from the registsered list?
    # ---------------------------------------------
    def del_admin(self, admin_id: str):
        admin_list = self.get_admins()
        if admin_list is None:
            self.glogger.error("The admin list is None. Cannot delete admin: %s", admin_id)
            return False
        if not admin_id in admin_list:
            self.glogger.error("The admin %s does not exist in the admin list", admin_id)
            return False
        admin_list = [x for x in admin_list if x != admin_id]
        self._store_admins_list(admin_list)
        return True

    # ---------------------------------------------
    # Get the list of the admins?
    # ---------------------------------------------
    def get_admins(self):
        if self._admins is None:
            self._admins = self._get_admins_list()
        if self._admins is None:
            self.glogger.error("The admin list is None. No admin is registered")
            return None
        return self._admins

