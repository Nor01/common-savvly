import time
from common.util.logging_helper import get_logger
from common.database.db_wrapper import dbwrapper_connect
from common.controllers.firmvaluemarket import *
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# -----------------------------------
# Create an instrance of the logger
# -----------------------------------
glogger = get_logger()

# -----------------------------------
# The Houskeeper handler
# -----------------------------------
gscheduler = None

# -----------------------------------
# The cosmos handler
# -----------------------------------
_gcosmos = None


# --------------------------------------------------------------------------------
# Initialize the house-keeper
# ---------------------------------------------------------------------------------
def housekeeper_init():
    global gscheduler
    housekeeper_job_db_connect()  # Connect for the first time
    gscheduler = BackgroundScheduler(daemon=True, timezone="America/New_York")
    gscheduler.add_job(housekeeper_job_db_connect, 'interval', minutes=1)
    gscheduler.add_job(housekeeper_job_update_fmv, 'interval', minutes=6000)  # This is instead of FMV docker
    gscheduler.add_job(housekeeper_job_new_signed_contracts, 'interval', hours=1)  # Process the new sgned contracts
    # gscheduler.add_job(housekeeper_job_new_signed_contracts, 'interval', minutes=1)  # Process the new sgned contracts
    gscheduler.add_job(housekeeper_job_sync_storage_contracts, 'interval', hours=1)  # Sync the contracts on the storage
    gscheduler.add_job(housekeeper_job_upload_old_log_files, 'interval', hours=6)  # Upload the old log files to Azure
    # gscheduler.add_job(msgraphapp_refresh_token, 'interval', minutes=45)  # Refresh MS-Graph Access Token
    gscheduler.start()
    atexit.register(lambda: gscheduler.shutdown())  # Shut down the scheduler when exiting the app


# ---------------------------------------------------------------------------
# A job that is called by the Scheduler to keep the DB connection alive
# This job is called periodically (every 1 minute)
# ---------------------------------------------------------------------------
def housekeeper_job_db_connect():
    global _gcosmos
    glogger.debug("housekeeper_job_db_connect() called")
    if not _gcosmos:
        _gcosmos = dbwrapper_connect()
        return
    dbsession = _gcosmos.get_session()
    if not dbsession:
        glogger.info("The COSMOS DB session is None. Trying to reconnect to the DB")
        _gcosmos.connect_to_db()


# ---------------------------------------------------------------------------
# A job that is called by the Scheduler to update the FMV (Firm Value Market)
# of all users
# ---------------------------------------------------------------------------
def housekeeper_job_update_fmv():
    glogger.debug("housekeeper_job_update_fmv() is called to update the FMV of all the users")
    # fmv = FirmMarketValue()
    # fmv.get_and_update()


# ---------------------------------------------------------------------------
# Check if they are new signed contracts, if they are, add the new client
# To the active directory and database
# ---------------------------------------------------------------------------
from newuser.newuser import *
from common.controllers.contract import CheckForNewSignedContracts


def housekeeper_job_new_signed_contracts():
    # client_info = {'firstname': 'YYY', 'lastname': 'YYYYYY', 'email': 'YYY@leupus.com', 'address': 'YYYYYY',
    #                'zip_code': '21121', 'birthdate': '1998-07-03', 'sex': 'M', 'is_US_citizen': 'Y', 'is_married': 'Y',
    #                'ssn': '123-12-3123',
    #                'spouse_firstname': 'YYY', 'spouse_lastname': 'YYY', 'spouse_birthdate': '1999-07-11',
    #                'spouse_sex': 'F',
    #                'spouse_ssn': '123-12-3123', 'spouse_is_US_citizen': 'Y', 'spouse_address': 'YYYYYYYYY',
    #                'spouse_email': 'YYY@leupus.com', 'investment_start_date': '2022-07-11', 'payout_ages': [70],
    #                'ETF': 'VOO Vanguard', 'funding': '100000', 'purchaser_type': 'Qualified Purchaser'}
    client_infos = CheckForNewSignedContracts()
    for client_info in client_infos:
        glogger.info("Signed contract found!! adding new user:%s", client_info)
        result = NewUser().process_new_signed_client(client_info)
        glogger.info("Result %s of adding new client:%s", result, client_info)


# ---------------------------------------------------------------------------
# Check if the contract file exists on the Storage
# If not, upload it
# ---------------------------------------------------------------------------
from common.controllers.sync_storage_contract import *


def housekeeper_job_sync_storage_contracts():
    SyncStorageContract().sync()


# ---------------------------------------------------------------------------
# Upload the old log files to the Azure Storage
# ---------------------------------------------------------------------------
from common.controllers.logfiles_storage import *


def housekeeper_job_upload_old_log_files():
    LogFilesStorage().upload_old_log_files()
