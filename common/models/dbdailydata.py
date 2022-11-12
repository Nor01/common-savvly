import time
from datetime import datetime
from common.util.logging_helper import get_logger
from common.util.utility_functions import  utils_get_current_epoch_time
from common.database.db_tablecollection import *

# -----------------------------------------------------------------------------------------------------------------------
# User Data
# -----------------------------------------------------------------------------------------------------------------------
class DbDailyData(DbTableCollection):
    tab_name_daily = "daily"

    col_name_date = "date"
    col_name_share_cost = "share_cost"
    col_name_tot_portfolio = "tot_portfolio"
    col_name_lastupdate = "lastupdate"

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbDailyData")
        tables_info = self._build_tables_info()
        tables_attributes = self._build_tables_attributes()
        super().__init__(tables_info, tables_attributes)

    # ----------------------------------------------------------------------
    # Create a dictionary of the tables and columns
    # ----------------------------------------------------------------------
    def _build_tables_info(self):
        tables_info = {}

        tables_info[self.tab_name_daily] =  [
                                  (self.col_name_date, "text PRIMARY KEY"),
                                  (self.col_name_share_cost, "text"),
                                  (self.col_name_tot_portfolio, "text"),
                                  (self.col_name_lastupdate, "text"),
                                  ]
        return tables_info

    # ----------------------------------------------------------------------
    # Create a dictionary of the tables attributes
    # ----------------------------------------------------------------------
    def _build_tables_attributes(self):
        tables_attributes = {}
        tables_attributes[self.tab_name_daily] = { "create" : "CLUSTERING ORDER BY (" + self.col_name_date + " DESC)" }
        return tables_attributes

    # -----------------------------------
    # Add new day
    # -----------------------------------
    def update_today_values(self, share_cost:float = 0.0, tot_portfolio:float = 0.0):
        primekey = self._build_primary_key()
        if self.add_new_idx(primekey) == False:
            return False

        data_dict = {}
        data_dict[self.col_name_share_cost] = str(share_cost)
        data_dict[self.col_name_tot_portfolio] = str(tot_portfolio)
        data_dict[self.col_name_lastupdate] = utils_get_current_epoch_time()
        return self.update_values(primekey, self.tab_name_daily, data_dict)

    # ---------------------------------------------
    # Get Today's values
    # ----------------------------------------------
    def get_today_values(self):
        primekey = self._build_primary_key()
        values = self.get_table_row_values(primekey, self.tab_name_daily)
        self.glogger.debug(values)
        return values

    # ---------------------------------------------
    # Get all share cost and total portfolio
    # ----------------------------------------------
    def get_all_portfolio_values(self):
        value_list = self.get_table_data_per_colnames(self.tab_name_daily,
                                                      [self.col_name_date,
                                                       self.col_name_share_cost,
                                                       self.col_name_tot_portfolio])
        # print(value_list)
        return value_list

    # ---------------------------------------------
    # Get cost of the share
    # ----------------------------------------------
    def get_share_cost(self) -> float:
        values = self.get_values_last_row_by_idx()
        if not values:
            self.glogger.error("Could not get the value of the share toady - the database is empty")
            return 0.0
        print(values)
        print(type(values))
        share_cost_str = values[self.col_name_share_cost]
        try:
            share_cost = float(share_cost_str)
        except Exception as err:
            self.glogger.error.error("The share cost in the database is not a float number:%s err=%s", share_cost_str, err)
            return 0.0
        return share_cost

    # ---------------------------------------------
    # Get the value of the total portfolio
    # ----------------------------------------------
    def get_tot_portfolio(self) -> float:
        values = self.get_values_last_row_by_idx()
        if not values:
            self.glogger.error("Could not get the value of the portfolio - the database is empty")
            return 0.0
        tot_portfolio_str = values[self.col_name_tot_portfolio]
        try:
            tot_portfolio = float(tot_portfolio_str)
        except Exception as err:
            self.glogger.error("The total portfolio  in the database is not a float number:%s. err=%s", tot_portfolio_str, err)
            return 0.0
        return tot_portfolio

    # -----------------------------------
    # build Date
    # -----------------------------------
    def _build_primary_key(self):
        today = datetime.now()
        primekey = today.strftime("%Y%m%d%H%M%S%f")[:-3]
        return primekey

    # -----------------------------------
    # Get the update time
    # -----------------------------------
    #def _get_last_update_time(self):
    #    return str(int(time.time()))
