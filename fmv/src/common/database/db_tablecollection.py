from common.util.logging_helper import get_logger
from common.database.db_table import *
from common.database.db_wrapper import dbwrapper_get_db_session,  dbwrapper_connect
from common.util.performance import performance_start_timer, performance_print_took_time


# -----------------------------------------------------------------------------------------------------------------------
# A Group/Collection of tables
# -----------------------------------------------------------------------------------------------------------------------
class DbTableCollection:
    # ----------------------------------------------------------------------
    # Constructor
    # tables_columns is dictionary. The keys are the table names.
    # The values are the LIST of the tuples.
    # Every tuple is the column name and colum type
    # {   "tab1":[("col1", "text PRIMARY KEY"), ("col2", "integer"), ("col3", "blob")],
    #      "tab2":[("col1", "integer PRIMARY KEY"), ("col2", "text"), ("col3", "text")] }
    # tables_attributes is dictionary. The keys are the table names.
    # The values are the dictionaries too.
    # {   "tab1": { create: "CLUSTERING ORDER BY (date)"},
    #      "tab2": None }
    # ----------------------------------------------------------------------
    def __init__(self, tables_columns : dict, tables_attributes:dict = None):
        self.glogger = get_logger()
        self.tables_attributes = tables_attributes
        self.initial_tables_columns = tables_columns
        self.initial_tables_names = self._build_initial_tables_name_list()
        if self._count_initial_tables() < 1:
            self.glogger.error("Invalid number of tables (%d) passed. At least 1 table is needed")
            return
        self.idx_colname = "idx"
        #self.table_name  = table_name.lower()
        #self.num_cols_list = num_cols_list
        #self.idx_colname = prim_col_name.lower()
        #self.num_levels = len(self.num_cols_list)  # Number of levels

        self.dbtables = list()                       # list of Tables
        if not self._create_tables():
            self.glogger.error("Failed to create tables in the DbItem Constructor")
            return


    # --------------------------------------------------------------------
    # Get Diagnostics
    # --------------------------------------------------------------------
    def get_diag(self, idx : str = None):
        info = {}
        info['NumTables']       = self._count_initial_tables()
        info['TableNames']      = self.initial_tables_names
        info['NumCols']         = self._count_initial_columns_count()
        info['schema']          = self._get_actual_tables_schema()
        #info['ColList']         = self.num_cols_list
        #info['Tables']          = self._get_table_names()
        #info['ErrCntr']         = self._get_error_counter()
        #info['Count']           = self._get_tables_count()
        #info['Columns']         = self.get_all_dbitems_tables_columns()
        self._place_initial_tables_columns_in_dict(info)  # Place the tables and column names in the dictionary
        if idx is not None:
            info['values']          = self.get_all_values(idx)
        return info

    # --------------------------------------------------------------------
    # Add New IDX to the database
    # --------------------------------------------------------------------
    def add_new_idx(self, idx : str):
        counter = 0
        for dbtbl in self.dbtables:
            if dbtbl.insert_record(idx):
                counter += 1
        if counter == len(self.dbtables):
            self.glogger.debug("A new IDX (%s) added to the database", idx)
            return True
        if counter == 0:
            self.glogger.debug("The IDX (%s) already exists in the database", idx)
            return True
        self.glogger.error("The IDX (%s) added to %d tables, but there are %d tables", idx, counter, len(self.dbtables))
        return False

    # --------------------------------------------------------------------
    # Update value in a table
    # col_num is the column index: 1..number of columns in that table
    # --------------------------------------------------------------------
    def update_value(self, idx : str, table_nameinx, col_nameinx, value : str):
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None: return False
        col_nameinx = self._get_column_name(table_nameinx, col_nameinx)
        if col_nameinx is None: return False
        self.glogger.info("Updating idx=%s table=%s col=%s value=%s", idx, dbtable.get_table_name(), col_nameinx, value)
        return dbtable.update_col_str_value(idx, col_nameinx, value)

    # --------------------------------------------------------------------
    # Update value in a table to all records
    # col_num is the column index: 1..number of columns in that table
    # --------------------------------------------------------------------
    def update_value_to_all_records(self, table_nameinx, col_nameinx, value : str):
        count_updates = 0
        idx_list = self.get_idx_list()
        for idx in idx_list:
            result = self.update_value(idx, table_nameinx, col_nameinx, value)
            if not result:
                self.glogger.info("Failed to update idx=%s table=%s col=%s value=%s", idx, table_nameinx, col_nameinx, value)
            else:
                count_updates += 1
        if count_updates == len(idx_list):
            return True
        return False

    # --------------------------------------------------------------------
    # Get value from a table
    # col_num is the column index: 1..number of columns in that table
    # --------------------------------------------------------------------
    def get_col_str_value(self, idx: str, table_nameinx, col_nameinx):
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None: return None
        return dbtable.get_col_str_value(idx, col_nameinx)

    # --------------------------------------------------------------------
    # Update values in a table
    # --------------------------------------------------------------------
    def update_values(self, idx : str, table_nameinx, dict_value : dict):
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None: return
        self.glogger.debug("Updating idx=%s table=%s value=%s", idx, dbtable.get_table_name(), dict_value)
        return dbtable.update_multi_cols(idx, dict_value)

    # ----------------------------------------------------------------------
    # Insert a record
    # ----------------------------------------------------------------------
    def _insert_blob(self, idx: str, table_nameinx, col_nameinx, value : str):
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None: return
        col_nameinx = self._get_column_name(table_nameinx, col_nameinx)
        if col_nameinx is None: return
        dbtable.insert_blob(idx, col_nameinx, value)

    # --------------------------------------------------------------------
    # Get values of a table
    # --------------------------------------------------------------------
    def get_rows_specific_col_value(self, table_nameinx, col_name, value) -> list:
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None: return None
        return dbtable.get_rows_specific_col_value(col_name, value)

    # --------------------------------------------------------------------
    # Get values of a table
    # --------------------------------------------------------------------
    def get_table_row_values(self, idx : str, table_nameinx) -> dict:
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None: return None
        dict_values = dbtable.get_row(idx)
        self.glogger.debug("Table %s idx=%s Value=%s", table_nameinx, idx, dict_values)
        return dict_values

    # --------------------------------------------------------------------
    # Get values of  the last record
    # --------------------------------------------------------------------
    def get_values_last_row_by_idx(self) -> dict:
        tablename = self.initial_tables_names[0]  # Assume all items found in the first table
        dbtable = self.get_table_handle(tablename)
        if dbtable is None: return None
        dict_values = dbtable.get_last_row_by_idx()
        self.glogger.info("Table %s Value=%s", tablename, dict_values)
        return dict_values

    # --------------------------------------------------------------------
    # Get values of all tables
    # --------------------------------------------------------------------
    def get_all_values(self, idx : str) -> list:
        values = list()
        for tablename in self.initial_tables_names:
            dic = self.get_table_row_values(idx, tablename)
            values.append(dic)
        return values

    # --------------------------------------------------------------------
    # Get the list of the dbitems
    # Returns the list of the 'keys' (IDX) from the first table
    # --------------------------------------------------------------------
    def get_idx_list(self):
        if not dbwrapper_get_db_session():
            self.glogger.error("There is no connection to the database")
            return None
        dbitems_list = list()
        tablename = self.initial_tables_names[0] # Assume all items found in the first table
        rows_list = self._get_table_data(tablename)
        if rows_list is None:
            self.glogger.error("Invalid list of rows (None). Apparently DB error")
            return None
        for row in rows_list:
            if not self.idx_colname in row:
                self.glogger.error("The key idx ID=%s was not found in the row: %s", self.idx_colname, str(row))
                continue
            dbitems_list.append(row[self.idx_colname])
        return dbitems_list

    # --------------------------------------------------------------------
    # Delete all tablecollections
    # --------------------------------------------------------------------
    def delete_all_dbitems(self):
        idx_list = self.get_idx_list()
        self.glogger.info("Deleting all the tablecollections. There are %d dbitems", len(idx_list))
        if not idx_list:
            return -1  # Error: no dbitem was deleted
        return self._delete_dbitem_list(idx_list)

     # --------------------------------------------------------------------
    # Get all tables of all dbitems
    # --------------------------------------------------------------------
    def get_all_tables(self):
        if not dbwrapper_get_db_session():
            self.glogger.error("There is no connection to the database")
            return None
        all_dbitems_tables = list()
        for tablename in self.initial_tables_names:
            rows_list = self._get_table_data(tablename)
            all_dbitems_tables.append(rows_list)
        return all_dbitems_tables

     # --------------------------------------------------------------------
    # Get all columns of all tables
    # --------------------------------------------------------------------
    def get_all_dbitems_tables_columns(self):
        if not dbwrapper_get_db_session():
            self.glogger.error("There is no connection to the database")
            return None
        all_tables_columns = list()
        for tbl in self.dbtables:
            colmn_list = tbl.get_column_types()
            all_tables_columns.append(colmn_list)
        return all_tables_columns

    # --------------------------------------------------------------------
    # Get Tables Schema
    # --------------------------------------------------------------------
    def _get_actual_tables_schema(self) -> dict:
        schema = {}
        for tbl in self.dbtables:
            col_names = tbl.get_column_names()
            tablename = tbl.get_table_name()
            schema[tablename] = col_names
        return schema

    # --------------------------------------------------------------------
    # Print all tables of all dbitems
    # --------------------------------------------------------------------
    def print_all_tables(self):
        for tbl in self.dbtables:
            col_names = tbl.get_column_names()
            #print(col_names)
            #tracker_values = tbl.get_tracker_all_rows()
            #tbl.print_all_rows_as_dict_list(tracker_values)
            dbitem_values = tbl.get_all_rows()
            tbl.print_all_rows_as_dict_list(dbitem_values)

    # --------------------------------------------------------------------
    # Delete a recored
    # --------------------------------------------------------------------
    def delete_record(self, idx : str):
        for tbl in self.dbtables:
            self.glogger.info("Deleting dbitem ID=%s from table=%s", idx, tbl.get_table_name())
            tbl.delete_record(idx)
        return True

    # --------------------------------------------------------------------
    # Delete all dbitem tables
    # --------------------------------------------------------------------
    def delete_tables(self):
        for tbl in self.dbtables:
            self.glogger.info("Deleting table=%s", tbl.get_table_name())
            tbl.drop_table()

    # --------------------------------------------------------------------
    # Create the tables
    # --------------------------------------------------------------------
    def _create_tables(self):
        start_time = performance_start_timer()
        self.glogger.debug("Creating TableCollection (%d) tables : %s", self._count_initial_tables(), self._count_initial_columns_count())
        result = self.__create_tables()
        performance_print_took_time(f"Creating TableCollection Tables", start_time)
        return result

    # --------------------------------------------------------------------
    # Create the tables
    # --------------------------------------------------------------------
    def __create_tables(self):
        for table_name in self.initial_tables_names:
            start_time = performance_start_timer()
            colinfo = self._get_initial_column_info(table_name)
            table_attribute = self._get_table_attributes(table_name)
            self.glogger.debug("Creating tablecollection %s with %s colums, with table_attribute=%s", table_name, colinfo, table_attribute)
            dbtable = DbTable(table_name, colinfo, table_attribute)
            if not dbtable.create_table():
                self.glogger.debug("Failed to create tablecollection table %s.", table_name)
                return False
            performance_print_took_time(f"Creating table %s" % table_name, start_time)
            start_time = performance_start_timer()
            self.dbtables.append(dbtable)
            #self._create_columns(dbtable, level, self.num_cols_list[level])
            performance_print_took_time(f"Creating cols of table %s" % table_name, start_time)
        return True

    # --------------------------------------------------------------------
    # Get table attributes
    # --------------------------------------------------------------------
    def _get_table_attributes(self, table_name):
        if self.tables_attributes is None:
            return None
        if table_name in self.tables_attributes:
            return self.tables_attributes[table_name]
        return None

    # --------------------------------------------------------------------
    # Delete a list of dbitems
    # --------------------------------------------------------------------
    def _delete_dbitem_list(self, idx_list : list):
        count = 0
        for idx in idx_list:
            self.glogger.info("Deleting dbitems ID=%s", idx)
            self.delete_record(idx)
            count += 1
        return count

    # --------------------------------------------------------------------
    # Get the table names as a list
    # --------------------------------------------------------------------
    def _get_table_names(self) -> list:
        tblist = list()
        for tbl in self.dbtables:
            tblist.append(tbl.get_table_name())
        return tblist

    # --------------------------------------------------------------------
    # Get the errors of each table
    # --------------------------------------------------------------------
    def _get_error_counter(self) -> list:
        errlist = list()
        for tbl in self.dbtables:
            errlist.append(tbl.get_error_counter())
        return errlist

    # --------------------------------------------------------------------
    # Get the names of all tales in the schemma
    # --------------------------------------------------------------------
    def get_keyspace_tables_names(self) -> list:
        tablename = self.initial_tables_names[0]  # Assume all items found in the first table
        dbtable = self.get_table_handle(tablename)
        if dbtable is None: return None
        return dbtable.get_keyspace_tables_names()

    # --------------------------------------------------------------------
    # Build dbitem table name
    # --------------------------------------------------------------------
    #def _build_table_name(self, level:int):
    #    table_name = self.table_name + "_" + str(level + 1)  # must be lower case
    #    return table_name

    # --------------------------------------------------------------------
    # Create the columns of a give table
    # --------------------------------------------------------------------
    #def _create_columns(self, dbtable, level, num_cols) -> list:
    #    col_count = dbtable.get_extended_column_count()
    #    if  col_count >= num_cols:
    #        self.glogger.debug("There are already %d cols in the table %s. No need to create %d columns", col_count, dbtable.get_table_name(), num_cols)
    #        return False
    #    num_cols = num_cols - col_count
    #    for col in range(num_cols):
    #        col_type = self._get_create_column_type(level+1, col+1)
    #        col_name = dbtable.add_new_column(col_type)
    #        self.glogger.debug("Created column %s in dbitems table %s", col_name, dbtable.get_table_name())
    #    return True

    # --------------------------------------------------------------------
    # Get the type of the colum to be created
    # The options: text, blob
    # This function is usually overriden by the children of this class
    # --------------------------------------------------------------------
    #def _get_create_column_type(self, level, column_inx) -> str:
    #    return "text"

    # --------------------------------------------------------------------
    # Return a list of the number of records in the tables
    # --------------------------------------------------------------------
    def _get_tables_count(self) -> list:
        counts = list()
        for tbl in self.dbtables:
            count = tbl.count_records()
            counts.append(count)
        return counts

    # --------------------------------------------------------------------
    # Validate Table and Column number
    # Level is the table index   : 1..self.num_levels
    # --------------------------------------------------------------------
    #def _validate_table_number(self, level):
    #    if level < 1 or level > self.num_levels:
    #        self.glogger.error("Invalid level (table number): %d (allowed 1-%d)", level, self.num_levels)
    #        return False
    #    if level > len(self.dbtables):
    #        self.glogger.error("SW Error. Expected for %d tables in the array to match the level %d", len(self.dbtables), level)
    #        return False
    #    return True

    # --------------------------------------------------------------------
    # Validate Table and Column number
    # Level is the table index   : 1..self.num_levels
    # col_num is the column index: 1..number of columns in that table
    # --------------------------------------------------------------------
    #def _validate_col_number(self, level, col_num):
    #    num_colums = self.num_cols_list[level - 1]
    #    if col_num < 1 or col_num > num_colums:
    #        self.glogger.error("Invalid column number %d for table %d (allowed 1-%d)", col_num, level, num_colums)
    #        return False
    #    return True

    # --------------------------------------------------------------------
    # Get the rows of a specific table
    # --------------------------------------------------------------------
    def _get_table_data(self, tablenameinx) -> list:
        tbl = self.get_table_handle(tablenameinx)
        if tbl is None: return None
        dbitem_values = tbl.get_all_rows()
        rows_list = tbl.convert_rows_to_dict_list(dbitem_values)
        return rows_list

    # --------------------------------------------------------------------
    # Get the rows of a specific table per column names
    # --------------------------------------------------------------------
    def get_table_data_per_colnames(self, tablenameinx, colnames:list) -> list:
        tbl = self.get_table_handle(tablenameinx)
        if tbl is None: return None
        dbitem_values = tbl.get_all_rows()
        rows_list = tbl.convert_rows_to_value_list_per_colnames(dbitem_values, colnames)
        return rows_list

    # --------------------------------------------------------------------
    # Build an array of the tables name (initial)
    # --------------------------------------------------------------------
    def _build_initial_tables_name_list(self) -> list:
        table_names = []
        for tablename in self.initial_tables_columns.keys():
            #print(tablename)
            table_names.append(tablename)
        return table_names

    # --------------------------------------------------------------------
    # Get the number of initial tables
    # --------------------------------------------------------------------
    def _count_initial_tables(self) -> int:
        return len(self.initial_tables_names)

    # --------------------------------------------------------------------
    # Get the number of initial columns
    # --------------------------------------------------------------------
    def _count_initial_columns_count(self) -> list:
        colcount = []
        for tablename, colnames in self.initial_tables_columns.items():
            count = len(colnames)
            colcount.append(count)
        return colcount

    # --------------------------------------------------------------------
    # Get initial column count
    # --------------------------------------------------------------------
    def _get_initial_column_count(self, table_name:str) -> int:
        cols_info = self._get_initial_column_info(table_name)
        return len(cols_info)

    # --------------------------------------------------------------------
    # Get initial column info (pairs of col name and type)
    # --------------------------------------------------------------------
    def _get_initial_column_info(self, table_name:str) -> list:
        try:
            col_names = self.initial_tables_columns[table_name]
            return col_names
        except Exception as err:
            self.glogger.error("Could not find the list of column names for table %s", table_name)
        return []

    # --------------------------------------------------------------------
    # Get initial column names
    # --------------------------------------------------------------------
    def _get_initial_column_names(self, table_name:str) -> list:
        cols_info = self._get_initial_column_info(table_name)
        if not cols_info: # Empty or None
            return cols_info
        col_names  = []
        for col_info in cols_info:
            col_names.append(col_info[0])
        return col_names

    # --------------------------------------------------------------------
    # Place tables info in a passed dictionary
    # --------------------------------------------------------------------
    def _place_initial_tables_columns_in_dict(self, diag_dict: dict):
        for tablename, colnames in self.initial_tables_columns.items():
            diag_dict[tablename] = colnames

    # --------------------------------------------------------------------
    # Select Table
    # --------------------------------------------------------------------
    def get_table_handle(self, table_nameinx) -> DbTable:
        if isinstance(table_nameinx, int):
            if table_nameinx >= len(self.initial_tables_names):
                self.glogger.error("Invalid table index %d. Valid 0..%d", table_nameinx, len(self.initial_tables_names))
                return None
            return self.dbtables[table_nameinx]
        if not table_nameinx in self.initial_tables_names:
            self.glogger.error("table %s not found in the list", table_nameinx)
            return None
        inx = self.initial_tables_names.index(table_nameinx)
        return self.dbtables[inx]

    # --------------------------------------------------------------------
    # Select Column
    # --------------------------------------------------------------------
    def _get_column_name(self, table_nameinx, col_nameinx):
        dbtable = self.get_table_handle(table_nameinx)
        if dbtable is None:
            return None
        col_names = self._get_initial_column_names(table_nameinx)
        #print(col_names)
        if isinstance(col_nameinx, int):
            if col_nameinx >= len(col_names):
                self.glogger.error("Invalid col index %d. Valid 0..%d", col_nameinx, len(col_names))
                return None
            return col_names[col_nameinx]
        if not col_nameinx in col_names:
            self.glogger.error("Col %s not found in the list for table:%s", col_nameinx, table_nameinx)
            return None
        return col_nameinx