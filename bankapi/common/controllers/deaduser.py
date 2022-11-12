from common.controllers.dbhandles import *
from common.util.logging_helper import get_logger

# -----------------------------------
# Create an instance of the logger
# -----------------------------------
glogger = get_logger("deaduesr")

# -------------------------------------------------------------------------
# Distribute the shares of a dead user
# -------------------------------------------------------------------------
def deaduser_distribute_shares(deadidx : str, share_price: float):
    dbh = Dbhandles.get_instance()
    usertable = dbh.get_usertables()
    inheritance_table = dbh.get_inheritedtable()
    transfer_list = usertable.calculate_dead_user_shares_distribution(deadidx)
    if not transfer_list:
        glogger.error("Failed to calculate the distribution of the shares of the dead user:%s", deadidx)
        return False
    for transfer_data in transfer_list:
        idx = transfer_data[0]
        shares = transfer_data[1]
        result = usertable.update_inherited_shares(idx, shares)
        if not result:
            glogger.error("Failed to add %f inherited shares to the user %s, from dead:%s", shares, idx (deadidx))
        inheritance_table.add_new_inheritance(deadidx, idx, shares, share_price)
    #usertable.set_statusflag_closed(deadidx)