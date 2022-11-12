import base64
from datetime import datetime
from common.util.logging_helper import get_logger
from common.database.db_tablecollection import *
from common.util.utils_file_rw import *

# -----------------------------------------------------------------------------------------------------------------------
# Files Table
# -----------------------------------------------------------------------------------------------------------------------
class DbFiles(DbTableCollection):
    tab_name_files = "files"  # The database of files
    col_name_fileid = "idx"  # This is the primary key - must be "idx" - do not change it
    col_name_timestamp = "timestamp"  # When the file added
    col_name_file_description = "description"
    col_name_file_type = "type"
    col_name_file_owner = "owner"
    col_name_file_location = "location"

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self):
        self.glogger = get_logger("DbFiles")
        tables_info = self._build_tables_info()
        tables_attributes = self._build_tables_attributes()
        super().__init__(tables_info, tables_attributes)

    # -----------------------------------
    # Add new file record
    # -----------------------------------
    def add_contract(self, contract_id: str, description: str, owner: str, file_location: str):
        #filedata = utils_read_file(file_path)
        #if filedata is None:
        #    self.glogger.error("Failed to read the content of file=%s", file_path)
        #    return False
        #self.glogger.info("storing: file_id=%s file=%s, size=%d", file_id, file_path, len(filedata))
        #if self.add_new_idx(file_id) == False:
        #    return False
        info = {}
        info[self.col_name_timestamp] = self._build_timestamp()
        info[self.col_name_file_description] = description
        info[self.col_name_file_type] = "Contract"
        info[self.col_name_file_owner] = str(owner)
        info[self.col_name_file_location] = str(file_location)
        return self._update_file_info(contract_id, info)

    # ------------------------------------------
    # Get All Files Info
    # ------------------------------------------
    def get_all_files_info(self) -> list:
        value_list = self.get_table_data_per_colnames(self.tab_name_files, [self.col_name_fileid,
                                                                            self.col_name_timestamp,
                                                                            self.col_name_file_description,
                                                                            self.col_name_file_type,
                                                                            self.col_name_file_owner,
                                                                            self.col_name_file_location])
        return value_list

    # ------------------------------------------
    # Get File Data
    # ------------------------------------------
    #def get_file_data(self, fileid:str):
    #    filedata = self.get_col_str_value(fileid, self.tab_name_files, self.col_name_file_data)
    #    return filedata

    # ----------------------------------------------------------------------
    # Create the tables
    # ----------------------------------------------------------------------
    def _build_tables_info(self):
        tables_info = {}
        tables_info[self.tab_name_files] = [
            (self.col_name_fileid, "text PRIMARY KEY"),
            (self.col_name_timestamp, "text"),
            (self.col_name_file_description, "text"),
            (self.col_name_file_type, "text"),
            (self.col_name_file_owner, "text"),
            (self.col_name_file_location, "text"),
        ]
        return tables_info

    # ----------------------------------------------------------------------
    # Create a dictionary of the tables attributes
    # ----------------------------------------------------------------------
    def _build_tables_attributes(self):
        tables_attributes = {}
        tables_attributes[self.tab_name_files] = { "create" : "CLUSTERING ORDER BY (" + self.col_name_timestamp + " DESC)" }
        return tables_attributes

    # -----------------------------------------------------
    # Update the file info
    # -----------------------------------------------------
    def _update_file_info(self, fileid: str, data_dict: dict):
        return self.update_values(fileid, self.tab_name_files, data_dict)

    # -----------------------------------------------------
    # Update the file data
    # -----------------------------------------------------
    #def _update_file_data(self, fileid: str, value: str):
    #    return self._insert_blob(fileid, self.tab_name_files, self.col_name_file_data, value)

    # -----------------------------------
    # build DateTime
    # -----------------------------------
    def _build_timestamp(self):
        today = datetime.now()
        timestamp = today.strftime("%Y%m%d%H%M%S")
        return timestamp

#    # -------------------------------------------------------------------------------
#    # Serialize the data
#    # -------------------------------------------------------------------------------
#    def _serialize_data(self, filedata):
#        return filedata
#
#    # -------------------------------------------------------------------------------
#    # Deserialize the image
#    # -------------------------------------------------------------------------------
#    def _deserialize_data(self, db_data):
#        return db_data
#
#    # -------------------------------------------------------------------------------
#    # Store the image in the databse
#    # -------------------------------------------------------------------------------
#    def _store_image(self, userid: str, image_bytes):
#        try:
#            self.glogger.info("Storing image: %d bytes", len(image_bytes))
#            self.glogger.debug("Storing image: %s", image_bytes)
#            pic = Pictures()
#            pic.insert_picture(userid, image_bytes)
#        except Exception as err:
#            self.glogger.info("Failed to store the photo of this user: %s. err=%s", userid, err)
#            return False
#        return True
#
#    # -------------------------------------------------------------------------------
#    # Get the image from the databse
#    # -------------------------------------------------------------------------------
#    def _get_image(self, userid: str):
#        try:
#            pic = Pictures()
#            image_list = pic.get_picture(userid)
#            if len(image_list) < 1:
#                self.glogger.info("The list of the images for this user (%s) is empty", userid)
#                return None
#            image_bytes = image_list[0]  # get the first one
#            self.glogger.info("Retrieved image: %d bytes", len(image_bytes))
#            self.glogger.debug("Retrieved image: %s", image_bytes)
#        except Exception as err:
#            self.info("Failed to get the photo of this user: %s. err=%s", userid, err)
#            return None
#        return image_bytes
#
#    # -------------------------------------------------------------------------------
#    # Delete the image from the databse
#    # -------------------------------------------------------------------------------
#    def _delete_image(self, userid: str):
#        try:
#            pic = Pictures()
#            pic.delete_user(userid)
#        except Exception as err:
#            self.glogger.info("Failed to delete the photo of this user: %s. err=%s", userid, err)
#            return False
#        return True
#
#    # ----------------------------------------------------------------
#    # Store the image of the user
#    # ----------------------------------------------------------------
#    def ImageStore(self, userid: str, imagebase64):
#        self.glogger.info("Storing the image of the user %s - imagelen=%d", userid, len(imagebase64))
#        db_data = _serialize_image(imagebase64)
#        if not db_data:
#            return False
#        return _store_image(userid, db_data)
#
#    # ----------------------------------------------------------------
#    # Get the image of the user
#    # ----------------------------------------------------------------
#    def ImageGet(self, userid: str):
#        self.glogger.info("Getting the image of the user %s", userid)
#        db_data = _get_image(userid)
#        if not db_data:
#            self.glogger.error("The user %s has no photo", userid)
#            return None
#        imagebase64 = _deserialize_image(db_data)
#        return imagebase64
#
#    # ----------------------------------------------------------------
#    # delete the image of the user
#    # ----------------------------------------------------------------
#    def ImageDelete(self, userid: str):
#        self.glogger.info("Deleting the image of the user %s", userid)
#        return _delete_image(userid)
#
#    # ----------------------------------------------------------------
#    # Get the list of the pictures
#    # ----------------------------------------------------------------
#    def ImageGetPictureList(self):
#        self.glogger.info("Getting the list of the pictures")
#        pic = Pictures()
#        piclist = pic.get_all_pictures()
#        return piclist