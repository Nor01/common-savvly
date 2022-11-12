from  commontest import *  # Common to all tests in nthis repository
from  common.models.db_files import *
from  common.models.fs_files import *
from  common.models.azure_file_storage import *
from  common.controllers.contract_storage import *

# -------------------------------------------------------------------------
# Global variables
# -------------------------------------------------------------------------
glocalfolder = "C:\\Users\\Danny\\Downloads\\"
gfilename = "20220817_105300.jpg"
gurl="https://elinux.org/images/b/ba/Mlocke-elce2007-pmarch.pdf"
gfileid = gfilename
gfulllocalname = glocalfolder + gfilename

# -------------------------------------------------------------------------
# Show the list of the files on Azure
# -------------------------------------------------------------------------
def test_show_az_file_list():
    file_list = AzureFileStorage.get_instance().list_contracts()
    print(file_list)

# -------------------------------------------------------------------------
# Upload a file to azure
# -------------------------------------------------------------------------
def test_add_az_file():
    result = AzureFileStorage.get_instance().upload_contract(gfulllocalname)
    print(result)

# -------------------------------------------------------------------------
# Delete a file from azure
# -------------------------------------------------------------------------
def test_del_az_file():
    result = AzureFileStorage.get_instance().delete_contract(gfilename)
    print(result)

# -------------------------------------------------------------------------
# Download a file from azure
# -------------------------------------------------------------------------
def test_download_az_file():
    result = AzureFileStorage.get_instance().download_contract(gfilename)
    print(result)

# -------------------------------------------------------------------------
# Store a contract
# -------------------------------------------------------------------------
def test_store_contract():
    result = ContractStorage().store(gurl, gfileid, "Advisor", "Client", "client_id")
    print(result)

# -------------------------------------------------------------------------
# Show the list of the files from the database
# -------------------------------------------------------------------------
def test_show_db_file_list():
    file_list = DbFiles().get_all_files_info()
    print(file_list)

# -------------------------------------------------------------------------
# Add file to the DB
# -------------------------------------------------------------------------
def test_add_db_file():
    result = DbFiles().add_contract(gfileid, "test file", "danny", glocalfolder)
    print(result)

# -------------------------------------------------------------------------
# Delete file from the DB
# -------------------------------------------------------------------------
def test_del_db_file():
    result = DbFiles().delete_record(gfileid)
    print(result)

# -------------------------------------------------------------------------
# Delete/Drop the file table from the database
# -------------------------------------------------------------------------
def test_drop_db_file_table():
    result = DbFiles().delete_tables()
    print(result)

# -------------------------------------------------------------------------
# Show the list of the files in the upload folder on FS
# -------------------------------------------------------------------------
def test_show_fs_uploaded_file_list():
    file_list = FsFiles().list_uploaded_files()
    print(file_list)

# -------------------------------------------------------------------------
# Delete ALL uploaded files from the FS
# -------------------------------------------------------------------------
def test_delete_fs_uploaded_files():
    result = FsFiles().delete_uploaded_files(".jjj")
    print(result)

# -------------------------------------------------------------------------
# Delete an uploaded file from the FS
# -------------------------------------------------------------------------
def test_delete_fs_uploaded_file():
    result = FsFiles().delete_uploaded_files(gfilename)
    print(result)

# -------------------------------------------------------------------------
# Download Log File
# -------------------------------------------------------------------------
def test_download_log_file():
    result = FsFiles().download_logfile()
    print(result)

# -------------------------------------------------------------------------
# Download a file from a URL
# -------------------------------------------------------------------------
def test_download_url_file():
    result = FsFiles().download_url_file(gurl, "test_downloaded_file.xxx")
    print(result)

# -------------------------------------------------------------------------
# Show the list of the files in the download folder on FS
# -------------------------------------------------------------------------
def test_show_fs_downloaded_file_list():
    file_list = FsFiles().list_downloaded_files()
    print(file_list)

# -------------------------------------------------------------------------
# Delete ALL downloaded files from the FS
# -------------------------------------------------------------------------
def test_delete_fs_downloaded_files():
    result = FsFiles().delete_downloaded_files(".jjj")
    print(result)

# -------------------------------------------------------------------------
# Delete an downloaded file from the FS
# -------------------------------------------------------------------------
def test_delete_fs_downloaded_file():
    result = FsFiles().delete_downploaded_files(gfilename)
    print(result)



#-------------------------------------------------------------------------
# The lookup table for the supported test functions
#-------------------------------------------------------------------------
gtest_functions = [
    ["Exit",                                                                 test_exit],

    ["Show Contracts list from Azure",                                       test_show_az_file_list],
    ["Add Contract to Azure",                                                test_add_az_file],
    ["Delete Contract from Azure",                                           test_del_az_file],
    ["Download Contract from Azure",                                         test_download_az_file],
    ["Store a Contract on Savvly System",                                    test_store_contract],

    ["Show files list from the DB",                                          test_show_db_file_list],
    ["Add file to the DB",                                                   test_add_db_file],
    ["Delete file from the DB",                                              test_del_db_file],
    ["Delete the File Table from the DB",                                    test_drop_db_file_table],

    ["Show uploaded files list from the FS",                                 test_show_fs_uploaded_file_list],
    ["Delete ALL uploaded files from the FS",                                test_delete_fs_uploaded_files],
    ["Delete an uploaded file from the FS",                                  test_delete_fs_uploaded_file],

    ["Download log file from FS",                                            test_download_log_file],
    ["Download a file from a URL",                                           test_download_url_file],
    ["Show downloaded files list from the FS",                               test_show_fs_downloaded_file_list],
    ["Delete ALL downloaded files from the FS",                              test_delete_fs_downloaded_files],
    ["Delete an downloaded file from the FS",                                test_delete_fs_downloaded_file],

    #["Reserved",                                                             test_stub],
]

#-------------------------------------
# The program starts here
#-------------------------------------
if __name__ == "__main__":
    test_run_menu(gtest_functions)
