from common.util.logging_helper import get_logger
from common.models.dbusertables import *
from common.models.dbdailydata import *
from common.models.dbtransactions import *
from common.models.dbinherited import *
from common.models.db_ria_table import *
from common.models.db_potential_clients import *


# -----------------------------------------------------------------------------------------------------------------
# Get handles to the database tables
# -----------------------------------------------------------------------------------------------------------------
# noinspection SpellCheckingInspection
class Dbhandles:
    __instance = None

    ## ---------------------------------------------
    ## Return the singletone object
    ## ---------------------------------------------
    @staticmethod
    def get_instance():  # Static access method.
        if Dbhandles.__instance is None:
            Dbhandles()
        return Dbhandles.__instance

    # ---------------------------------------------
    # Constructor
    # ---------------------------------------------
    def __init__(self):
        if Dbhandles.__instance != None:
            raise Exception("This class is a singleton!")
            return
        Dbhandles.__instance = self
        self.glogger = get_logger("Dbhandles")
        self.usertables = None
        self.dailytable = None
        self.transactiontable = None
        self.inheritedtable = None
        self.RIAtables = None
        self.potential_clients_table = None

    # -----------------------------------
    # Delete Daily tables
    # -----------------------------------
    def delete_daily_datatable(self):
        self.get_dailydatatable().delete_tables()
        self.set_dailydatatable(None)

    # -----------------------------------
    # Delete Transaction tables
    # -----------------------------------
    def delete_transactiontable(self):
        self.get_transactiontable().delete_tables()
        self.set_transactiontable(None)

    # -----------------------------------
    # Delete inherite tables
    # -----------------------------------
    def delete_inheritetable(self):
        self.get_inheritedtable().delete_tables()
        self.set_inheritedtable(None)

    # -----------------------------------
    # Delete potential clients tables
    # -----------------------------------
    def delete_potential_clients_tables(self):
        self.get_potential_clients_tables().delete_tables()
        self.set_potential_clients_tables(None)

    # -----------------------------------
    # Delete RIA tables
    # -----------------------------------
    def delete_RIA_tables(self):
        self.get_RIAtables().delete_tables()
        self.set_RIAtables(None)

    # -----------------------------------
    # Delete USER tables
    # -----------------------------------
    def delete_user_tables(self):
        self.get_usertables().delete_tables()
        self.set_usertables(None)

    # -----------------------------------
    # Delete all tables
    # -----------------------------------
    def delete_all_tables(self):
        self.delete_daily_datatable()
        self.delete_transactiontable()
        self.delete_inheritetable()
        self.delete_potential_clients_tables()
        self.delete_RIA_tables()
        self.delete_user_tables()

    # -----------------------------------
    # Get the UserTables object
    # -----------------------------------
    def get_usertables(self) -> DbUserTables:
        if self.usertables is None:
            self.usertables = DbUserTables()
        return self.usertables

    # -----------------------------------
    # Set the UserTables object
    # -----------------------------------
    def set_usertables(self, usertables: DbUserTables):
        self.usertables = usertables

    # -----------------------------------
    # Get the RIATables object
    # -----------------------------------
    def get_RIAtables(self) -> DbRIATables:
        if self.RIAtables is None:
            self.RIAtables = DbRIATables()
        return self.RIAtables

    # -----------------------------------
    # Get the potential customer Tables object
    # -----------------------------------
    def get_potential_clients_tables(self) -> DbPotentialClientsTables:
        if self.potential_clients_table is None:
            self.potential_clients_table = DbPotentialClientsTables()
        return self.potential_clients_table

    # -----------------------------------
    # Set the potential client table
    # -----------------------------------
    def set_potential_clients_tables(self, potential_clients_table: DbPotentialClientsTables):
        self.potential_clients_table = potential_clients_table

    # -----------------------------------
    # Set the UserTables object
    # -----------------------------------
    def set_RIAtables(self, RIAtables: DbRIATables):
        self.RIAtables = RIAtables

    # -----------------------------------
    # Get the Daily Data object
    # -----------------------------------
    def get_dailydatatable(self) -> DbDailyData:
        if self.dailytable is None:
            self.dailytable = DbDailyData()
        return self.dailytable

    # -----------------------------------
    # Set the Daily Data object
    # -----------------------------------
    def set_dailydatatable(self, dailytable: DbDailyData):
        self.dailytable = dailytable

    # -----------------------------------
    # Get the Transaction object
    # -----------------------------------
    def get_transactiontable(self) -> DbTransactions:
        if self.transactiontable is None:
            self.transactiontable = DbTransactions()
        return self.transactiontable

    # -----------------------------------
    # Set the Transaction object
    # -----------------------------------
    def set_transactiontable(self, transactiontable: DbTransactions):
        self.transactiontable = transactiontable

    # -----------------------------------
    # Get the Inheritence object
    # -----------------------------------
    def get_inheritedtable(self) -> DbInherited:
        if self.inheritedtable is None:
            self.inheritedtable = DbInherited()
        return self.inheritedtable

    # -----------------------------------
    # Set the Inheritence object
    # -----------------------------------
    def set_inheritedtable(self, inheritedtable: DbInherited):
        self.inheritedtable = inheritedtable

    # -----------------------------------
    # Add new user
    # -----------------------------------
    # def add_new_user(self, idx:str, social:str, date_of_birth:str, address:str):
    #    usertables = self.get_usertables()
    #    return usertables.add_new_user(idx, social, date_of_birth, address)

    # ------------------------------------------
    # Activate the User
    # ------------------------------------------
    # def activate_user(self, idx: str):
    #    usertables = self.get_usertables()
    #    return usertables.activate_user(idx)

    # ------------------------------------------
    # Deactivate the User
    # ------------------------------------------
    # def deactivate_user(self, idx: str):
    #    usertables = self.get_usertables()
    #    return usertables.deactivate_user(idx)

    # -----------------------------------
    # get user data
    # -----------------------------------
    # def get_user_data(self, idx:str) -> list:
    #    usertables = self.get_usertables()
    #    data_list = usertables.get_all_values(idx)
    #    return data_list
