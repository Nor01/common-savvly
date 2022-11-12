import sys
from datetime import datetime
import time
from common.util.logging_helper import get_logger
from common.controllers.dbhandles import *

# ----------------------------------------------------------------------------------------------------------------------
# The FMV class
# ----------------------------------------------------------------------------------------------------------------------
class FirmMarketValue:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("fmv")
        self.dbhandle = Dbhandles.get_instance()
        self.usertable = self.dbhandle.get_usertables()
        self.dailytable = self.dbhandle.get_dailydatatable()

    # ----------------------------------------------------------------------
    # Run forever
    # ----------------------------------------------------------------------
    def run_forever(self):
        sec_counter = 0
        sleep_timeout = 60  # 1 minute
        fmv_timeout = (1 * sleep_timeout)  # 5 minutes
        max_timeout = fmv_timeout
        while True:
            if sec_counter == fmv_timeout:  # 5 minutes passed
                self.get_and_update()
            time.sleep(sleep_timeout)  # sleep 1 minute
            sec_counter += sleep_timeout
            if sec_counter > max_timeout:
                sec_counter = 0

    # ----------------------------------------------------------
    # Update Daily value - Called by BankAdaptor or Trader
    # ----------------------------------------------------------
    def update_today_values(self, share_cost: float, tot_portfolio: float): return self.dailytable.update_today_values(share_cost, tot_portfolio)

    # ----------------------------------------------------------------------
    # Get and Update the share cost to all users
    # ----------------------------------------------------------------------
    def get_and_update(self):
        sharecost = self.dailytable.get_share_cost()    # Get the value from daily table
        if sharecost < 0:
            self.glogger.error("The cost of the share is invalid: %f", sharecost)
            return
        self.glogger.info("Updating the share-cost %f to all users", sharecost)
        self._debug_print(sharecost)
        self.usertable.update_all_fmvs(sharecost)       # Update all users

    # ----------------------------------------------------------------------
    # Debug print - Debug only
    # ----------------------------------------------------------------------
    def _debug_print(self, sharecost):
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string + " SharePrice=" + str(sharecost))
        sys.stdout.flush()  # Debug only
