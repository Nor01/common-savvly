from common.util.config_wrapper import config_log_cql_commands, get_config_int_param
from common.database.db_wrapper import dbwrapper_get_db_session, dbwrapper_get_db_keyspace_name, dbwrapper_connect
from common.util.logging_helper import get_logger
from common.util.performance import performance_start_timer, performance_print_took_time

# -----------------------------------------------------------------------------------------------------------------------
# A PARENT Database Table
# -----------------------------------------------------------------------------------------------------------------------
class DbTable:
    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self, table_name:str, columns_info : list, table_attributes:dict = None, is_extendable=False):
        self.glogger = get_logger("DbTable")
        self.table_subname = table_name.lower()
        self.table_name = self.table_subname
        self.dbsession = None
        self.keyspace = None
        self.columns_info = columns_info
        self.table_attributes = table_attributes
        self.is_extendable = is_extendable
        self.tarcker_table = None
        self.query_err_cntr = 0

    # --------------------------------------------------------------------
    # Connect to the database
    # --------------------------------------------------------------------
    def create_table(self):
        dbsession = dbwrapper_get_db_session()
        if not dbsession:
            self.glogger.error("There is no connection to the DB yet (table=%s)", self.table_subname)
            return False
        self.dbsession = dbwrapper_get_db_session()
        self.keyspace = dbwrapper_get_db_keyspace_name()
        self.table_name = self.keyspace + "." + self.table_subname

        if len(self.columns_info) < 1:
            self.glogger.error("Invalid columns-info passed to create table %s. Required list of tuples(name, type)", self.table_name)
            return False

        throuput = get_config_int_param("table_thruput")
        extention = self._get_table_creation_attribute()
        self.glogger.debug("Creating Table %s. NumColumns=%d extention=%s", self.table_name, len(self.columns_info), extention)
        self._create_table(throughput=throuput, extention=extention)
        self._change_table_throughput(new_throughput=throuput)  #TBD
        # ---------------------------------------------------------------------
        # If this table extendable with more colums, create a tracker table
        # ---------------------------------------------------------------------
        if self.is_extendable:
            self.tarcker_table = self._create_tracker_table(self.table_subname)
        return True

    # ----------------------------------------------------------------------
    # Count the records in  the table
    # ----------------------------------------------------------------------
    def count_records(self) -> int:
        command = "SELECT COUNT(*) FROM  " + self.table_name
        rows = self._execute_db_command(command)
        if not rows:
            self.glogger.error("failed to get the number of records of table: %s", self.table_name)
            return -1
        count = self._format_row_as_single_int_scalar(rows)
        self.glogger.debug("There are %d records in the table: %s", count, self.table_name)
        return count

    # ----------------------------------------------------------------------
    # Check if a record exists in the table
    # ----------------------------------------------------------------------
    def record_exists(self, idx: str) -> bool:
        col1_name = self._get_first_column_name()
        command = "SELECT " + col1_name + " FROM  " + self.table_name + " WHERE " + col1_name + "= '" + str(idx) + "'"
        rows = self._execute_db_command(command)
        if not rows:
            self.glogger.debug("The ID=%s does NOT exist in the table: %s (rows empty)", idx, self.table_name)
            return False
        existing_id = self._format_row_as_single_string_scalar(rows)
        if not existing_id:
            self.glogger.debug("The ID=%s does NOT exist in the table: %s (id is None)", idx, self.table_name)
            return False
        self.glogger.debug("The ID=%s EXISTS in the table: %s", idx, self.table_name)
        return True

    # ----------------------------------------------------------------------
    # Insert a record to the table (userid only)
    # ----------------------------------------------------------------------
    def insert_record(self, idx: str):
        if self.record_exists(idx):
            self.glogger.debug("The ID=%s already exists in the table: %s", idx, self.table_name)
            return False # Not added - It already exists
        if self.tarcker_table:
            self.tarcker_table.insert_record(idx)   # Add this to the tracking table too
        col1_name = self._get_first_column_name()
        command = "INSERT INTO  " + self.table_name + " (" + col1_name + ") VALUES ('" + str(idx) + "')"
        result = self._execute_db_command(command)
        if result is None:
            return False
        self.glogger.debug("The ID=%s added to the table: %s", idx, self.table_name)
        return True

    # ----------------------------------------------------------------------
    # Insert a record to the table with a dictionary of colums & values
    # ----------------------------------------------------------------------
    def update_multi_cols(self, idx: str, dict_values : dict):
        query_syntax = self._build_update_query_syntax(dict_values)
        if not query_syntax:
            return False
        self.insert_record(idx)
        col1_name = self._get_first_column_name()
        command = "UPDATE " + self.table_name + query_syntax + " WHERE " + col1_name + " = '" + str(idx) + "'"
        result = self._execute_db_command(command)
        if result is None:
            return False
        return True

    # ----------------------------------------------------------------------
    # Insert a record to the table (UserID + Column Value)
    # ----------------------------------------------------------------------
    def update_col_str_value(self, idx: str, column, value):
        col_name = self._convert_column_to_name(column)
        self.glogger.debug("Updating idx=%s Table=%s Column=%s value=%s", idx, self.table_name, col_name, value)
        if not self._column_exists(col_name):
            self.glogger.error("The Column=%s does not exist in the table: %s", col_name, self.table_name)
            return False
        self.insert_record(idx)
        col1_name = self._get_first_column_name()
        command = "UPDATE " + self.table_name + " SET " + col_name + " = '" + str(value) + "' WHERE " + col1_name + " = '" + str(idx) + "'"
        result = self._execute_db_command(command)
        if result is None:
            return False
        return True

    # ----------------------------------------------------------------------
    # Insert a blob
    # ----------------------------------------------------------------------
    def insert_blob(self, idx: str, column, value : str):
        col1_name = self._get_first_column_name()
        col_name = self._convert_column_to_name(column)
        #command = "INSERT INTO  " + self.table_name + "  (" + col1_name + "," + col_name + ") VALUES ('" + str(idx) + "', '" + str(value) + "')"
        command = "INSERT INTO  " + self.table_name + "  (" + col1_name + "," + col_name + ") VALUES (%s, %s)"
        params = [idx, value]
        result = self._execute_db_command(command)
        if result is None:
            return False
        return True

    # ----------------------------------------------------------------------
    # Get a record to the table (UserID + Column Value)
    # ----------------------------------------------------------------------
    def get_col_str_value(self, idx: str, column) -> str:
        col_name = self._convert_column_to_name(column)
        rows = self._get_column_value(idx, col_name)
        if not rows:
            self.glogger.error("The ID=%s does NOT exist in the table: %s (rows empty)", idx, self.table_name)
            return None
        value = self._format_row_as_single_string_scalar(rows)
        return value

    # ----------------------------------------------------------------------
    # Add a new column and return its name
    # Possible values for col_type: text, blob
    # ----------------------------------------------------------------------
    def add_new_column(self, col_type="text") -> str:
        next_col_name = self._build_next_column_name()
        if self._column_exists(next_col_name):
            self.glogger.error("Internal Error in table (%s). Supposed to create column %s, but it already exists", self.table_name, next_col_name)
            return None
        command = "ALTER TABLE " + self.table_name + " ADD " + next_col_name + " " + col_type
        self._execute_db_command(command)
        #print(self.get_column_names())
        return next_col_name

    # ----------------------------------------------------------------------
    # Get the names of all columns
    # ----------------------------------------------------------------------
    def get_column_names(self) -> list:
        command = "SELECT * FROM system_schema.columns WHERE keyspace_name = '" + self.keyspace + "' AND table_name = '" + self.table_subname + "'"
        rows = self._execute_db_command(command)
        names = list()
        for row in rows:
            #print(row)
            #print(type(row))
            names.append(row.column_name)
        return names

    # ----------------------------------------------------------------------
    # Get the types of all columns
    # ----------------------------------------------------------------------
    def get_column_types(self) -> list:
        command = "SELECT * FROM system_schema.columns WHERE keyspace_name = '" + self.keyspace + "' AND table_name = '" + self.table_subname + "'"
        rows = self._execute_db_command(command)
        types = list()
        for row in rows:
            #print(row)
            #print(type(row))
            info = [row.column_name, row.type]
            types.append(info)
        return types

    # ----------------------------------------------------------------------
    # Get the names of all tables in the schema
    # ----------------------------------------------------------------------
    def get_keyspace_tables_names(self) -> list:
        command = "SELECT * FROM system_schema.tables WHERE keyspace_name = '" + self.keyspace + "'"
        rows = self._execute_db_command(command)
        names = list()
        for row in rows:
            #print(row)
            #print(type(row))
            names.append(row.table_name)
        return names

    # ----------------------------------------------------------------------
    # Get the number of columns
    # ----------------------------------------------------------------------
    def get_extended_column_count(self) -> int:
        col_list = self.get_column_names()
        col_count = len(col_list)
        col_count = col_count - len(self.columns_info) #Subtract the fixed columns (userid)
        if col_count < 0:
            col_count = 0
        return col_count

    # ----------------------------------------------------------------------
    # Convert Rows to dictionary List
    # ----------------------------------------------------------------------
    def convert_rows_to_dict_list(self, rows) -> list:
        return self._convert_rows_to_dict_list(rows)

    # ----------------------------------------------------------------------
    # Convert Rows to Value List
    # ----------------------------------------------------------------------
    def convert_rows_to_value_list(self, rows) -> list:
        return self._convert_rows_to_value_list(rows)

    # ----------------------------------------------------------------------
    # Convert Rows to Value List per column names
    # ----------------------------------------------------------------------
    def convert_rows_to_value_list_per_colnames(self, rows, column_names:list) -> list:
        return self._convert_rows_to_value_list_per_colnames(rows, column_names)

    # ----------------------------------------------------------------------
    # Print the retrieved rows (cassandra.cluster.ResultSet)
    # ----------------------------------------------------------------------
    def print_all_rows_as_dict_list(self, rows):
        rows_list = self.convert_rows_to_dict_list(rows)
        for rec in rows_list:
            self.glogger.info("%s", rec)
        return rows_list

    # ----------------------------------------------------------------------
    # Print the retrieved rows (cassandra.cluster.ResultSet)
    # ----------------------------------------------------------------------
    def print_all_rows_as_value_list(self, rows):
        rows_list = self.convert_rows_to_value_list(rows)
        for inx in range(len(rows_list)):
            self.glogger.info("%s", str(rows_list[inx]))
        return rows_list

    # ----------------------------------------------------------------------
    # Get all rows of the table
    # ----------------------------------------------------------------------
    def get_all_rows(self) -> list:
        command = "SELECT * FROM  " + self.table_name + " ALLOW FILTERING"
        rows = self._execute_db_command(command)
        self.glogger.debug("%s Rows: TypeList=%s", self.table_name, type(rows))
        return rows


    # ----------------------------------------------------------------------
    # Get the last row (sort by IDX)
    # ----------------------------------------------------------------------
    def get_last_row_by_idx(self) -> dict:
        col1_name = self._get_first_column_name()
        #command = "SELECT * FROM  " + self.table_name + " ORDER BY  " + col1_name + " DESC LIMIT 1"
        command = "SELECT * FROM  " + self.table_name + " LIMIT 1"
        rows = self._execute_db_command(command)
        dict_values = self.convert_rows_to_dict_list(rows)
        if dict_values:
            dict_values = dict_values[0]
        return dict_values

    # ----------------------------------------------------------------------
    # Get all rows that have a specific value in a column
    # ----------------------------------------------------------------------
    def get_rows_specific_col_value(self, col_name: str, value:str) -> list:
        command = "SELECT * FROM  " + self.table_name + " WHERE " + col_name + "= '" + str(value) + "'" + " ALLOW FILTERING"
        rows = self._execute_db_command(command)
        dict_list = self.convert_rows_to_dict_list(rows)
        return dict_list

    # ----------------------------------------------------------------------
    # Get a specific row from the table
    # ----------------------------------------------------------------------
    def get_row(self, idx: str) -> dict:
        col1_name = self._get_first_column_name()
        dict_list = self.get_rows_specific_col_value(col1_name, str(idx))
        if dict_list:
            dict_list = dict_list[0]
        return dict_list
        #command = "SELECT * FROM  " + self.table_name + " WHERE " + col1_name + "= '" + str(idx) + "'"
        #rows = self._execute_db_command(command)
        #dict_values = self.convert_rows_to_dict_list(rows)
        #if dict_values:
        #    dict_values = dict_values[0]
        #return dict_values

    # ----------------------------------------------------------------------
    # Get all rows of the Tracker table
    # ----------------------------------------------------------------------
    def get_tracker_all_rows(self) -> list:
        if not self.tarcker_table:
            self.glogger.error("This table (%s) is not extendable. It does not have a tracker table", self.table_name)
            return None
        return self.tarcker_table.get_all_rows()

    # ----------------------------------------
    # Delete a user record
    # ----------------------------------------
    def delete_record(self, idx: str):
        col1_name = self._get_first_column_name()
        command = "DELETE FROM " + self.table_name + " WHERE " + col1_name + "= '" + str(idx) + "'"
        self._execute_db_command(command)

    # ----------------------------------------------------------------------
    # Delete the table
    # ---------------------------------------------------------------------
    def drop_table(self):
        if self.tarcker_table:
            self.tarcker_table.drop_table()
        command = 'DROP TABLE IF EXISTS ' + self.table_name
        self._execute_db_command(command)

    # --------------------------------------------------------------------
    # Get table name
    # --------------------------------------------------------------------
    def get_table_name(self): return self.table_name

    # --------------------------------------------------------------------
    # Get the counter of the errors
    # --------------------------------------------------------------------
    def get_error_counter(self): return self.query_err_cntr

    # --------------------------------------------------------------------
    # Excecute a command
    # --------------------------------------------------------------------
    def _execute_db_command(self, command : str, params=None):
        if not self.dbsession:
            self.glogger.error("There is no connection to the DB yet (table=%s) - cannot execute command", self.table_subname)
            return None
        if config_log_cql_commands():
            self.glogger.info(command)
        try:
            result = self.dbsession.execute(timeout=100, query=command, parameters=params)
        except Exception as err:
            self.query_err_cntr += 1
            self.glogger.error("Failed to run command: %s. err=%s", command, err)
            return None
        return result

    # --------------------------------------------------------------------
    # Create A Tracker Table
    # Return DbTable Object type
    # --------------------------------------------------------------------
    def _create_tracker_table(self, table_name:str):
        columns_info = [("TrUid",  "text PRIMARY KEY"),
                        ("maxcol", "int")]
        table_name = table_name + "_tracker"
        dbtable = DbTable(table_name, columns_info, is_extendable=False)
        if not dbtable.create_table():
            self.glogger.error("Failed to connect to the datbase and create table %s", table_name)
            return None
        return dbtable

    # ----------------------------------------------------------------------------
    # Create a Tracker Table
    # ----------------------------------------------------------------------------
    def _build_columns_query_syntax(self, columns_info: list):
        query_syntax = " ("
        for col_info in columns_info:
            colname = col_info[0]
            colname = colname.lower()
            coltype = col_info[1]
            self.glogger.debug("col_info: %s. Create col=%s type=%s", col_info, colname, coltype)
            query_syntax = query_syntax + " " + colname + " " + coltype + "," # Add name and Type
        query_syntax = query_syntax[:-1]
        query_syntax = query_syntax + ") "
        return query_syntax

    # --------------------------------------------------------------------
    # Get create-table attribute from the passed attributes
    # --------------------------------------------------------------------
    def _get_table_creation_attribute(self) -> str:
        if self.table_attributes is None:
            return None
        if "create" in self.table_attributes:
            return self.table_attributes["create"]
        return None

    # ----------------------------------------------------------------------
    # Create the table
    # ----------------------------------------------------------------------
    def _create_table(self, throughput, extention:str=None):
        start_time = performance_start_timer()
        col_info = self._build_columns_query_syntax(self.columns_info)
        command = "CREATE TABLE IF NOT EXISTS " + self.table_name + col_info
        command += "WITH cosmosdb_provisioned_throughput=" + str(throughput)
        if extention:
            command += ", " + extention
        #print(command)
        result = self._execute_db_command(command)
        performance_print_took_time(f"Creating table %s" % self.table_name, start_time)
        return result

    # ----------------------------------------------------------------------
    # Convert Column Index to Column name (String)
    # ----------------------------------------------------------------------
    def _convert_column_to_name(self, column):
        if isinstance(column, int):
            return self._build_column_name(column)
        return column

    # ----------------------------------------------------------------------
    # Build update query syntax
    # ----------------------------------------------------------------------
    def _build_update_query_syntax(self, dict_values : dict) -> str:
        col_names = self.get_column_names()
        at_least_one_col_found = False
        query_syntax = " SET "
        for col_name, value in dict_values.items():
            if not col_name in col_names:
                self.glogger.error("The Column=%s does not exist in the table: %s", col_name, self.table_name)
                continue
            query_syntax = query_syntax + " " + col_name + " = '" + str(value) + "',"
            at_least_one_col_found = True
        if not at_least_one_col_found:
            self.glogger.error("No existing column found in the dictionary: %s to update table %s", dict_values, self.table_name)
            return None
        query_syntax = query_syntax[:-1]
        return query_syntax

    # ----------------------------------------------------------------------
    # Get the value of a column
    # ----------------------------------------------------------------------
    def _get_column_value(self, idx: str, col_name: str):
        col1_name = self._get_first_column_name()
        command = "SELECT " + col_name + " FROM  " + self.table_name + " WHERE " + col1_name + "='" + str(idx) + "'"
        rows = self._execute_db_command(command)
        return rows

    # ----------------------------------------------------------------------
    # Update Column Value
    # ----------------------------------------------------------------------
    def _update_col_int_value(self, idx, col_name : str, value):
        col1_name = self._get_first_column_name()
        command = "UPDATE " + self.table_name + " SET " + col_name + " = " + str(value) + " WHERE " + col1_name + "='" + str(idx) + "'"
        return self._execute_db_command(command)

    # ----------------------------------------------------------------------
    # Set/Chnage the Throughput of the table
    # ----------------------------------------------------------------------
    def _change_table_throughput(self, new_throughput: int):
        command = "ALTER TABLE " + self.table_name + " WITH cosmosdb_provisioned_throughput =" + str(new_throughput)
        return self._execute_db_command(command)

    # ----------------------------------------------------------------------
    # Get the name of the first column (of the tracker)
    # ----------------------------------------------------------------------
    def _get_first_column_name(self):
        col1_info = self.columns_info[0]  # Name , Type of the first column (IDX)
        return col1_info[0]

    # ----------------------------------------------------------------------
    # Get the name of the first column (of the tracker)
    # ----------------------------------------------------------------------
    def _get_tracker_first_column_name(self):
        col1_info = self.columns_info[0]  # Name , Type of the first column (IDX)
        return col1_info[0]

    # ----------------------------------------------------------------------
    # Get the name of the second column (of the tracker)
    # ----------------------------------------------------------------------
    def _get_tracker_second_column_name(self):
        if len(self.columns_info) < 2:
            self.glogger.error("Invalid columns-info passed to this table %s. At least two columns required)", self.table_name)
            return "Unknown"
        col2_info = self.columns_info[1]    # Name , Type of the first column (maxcol)
        return col2_info[0]

    # ----------------------------------------------------------------------
    # Insert the first colum to the table
    # ----------------------------------------------------------------------
    def _add_tracker_first_colum(self, idx: str):
        col1_name = self._get_tracker_first_column_name()
        col2_name = self._get_tracker_second_column_name()
        command = "INSERT INTO  " + self.table_name + "  (" + col1_name + "," + col2_name + ") VALUES ('" + str(idx) + "', 0)"
        self.glogger.debug("First column index in table %s", self.table_name)
        return self._execute_db_command(command)

    # ----------------------------------------------------------------------
    # Get the latest Column Index
    # ----------------------------------------------------------------------
    def _get_tracker_latest_column_inx(self, idx) -> int:
        col2_name = self._get_tracker_second_column_name()
        self.glogger.debug("Getting value of col=%s from table=%s idx=%s from the tracker table", col2_name, self.table_name, idx)
        rows = self._get_column_value(idx, col2_name)
        last_col_inx = self._format_row_as_single_int_scalar(rows)
        self.glogger.debug("Last column index in table %s is: %d", self.table_name, last_col_inx)
        return last_col_inx

    # ----------------------------------------------------------------------
    # Build column name from index
    # ----------------------------------------------------------------------
    def _build_column_name(self, column_inx):
        if column_inx < 0:
            return None
        return "_" + str(column_inx)

    # ----------------------------------------------------------------------
    # Build NEXT column name
    # ----------------------------------------------------------------------
    def _build_next_column_name(self):
        next_col = self._next_column_index()
        if next_col < 0:
            self.glogger.error("Failed to find the next dolumn index to build: %d", next_col)
            return None
        return self._build_column_name(next_col)

    # ----------------------------------------------------------------------
    # Get the latest Column Name
    # ----------------------------------------------------------------------
    def _get_tracker_latest_column_name(self, idx):
        last_col_inx = self._get_tracker_latest_column_inx(idx)
        if not last_col_inx or last_col_inx < 0:
            return None
        return self._build_column_name(last_col_inx)

    # ----------------------------------------------------------------------
    # Get the latest column index and increment the index
    # ----------------------------------------------------------------------
    def _add_tracker_new_colum_inx(self, idx) -> int:
        old_val = self._get_tracker_latest_column_inx(idx)
        if not old_val or old_val < 0 :
            self.glogger.debug("This table (%s) has no column - creating  the first one", self.table_name)
            self._add_tracker_first_colum(idx)
            old_val = 1
        else:
            old_val = old_val + 1
        col2_name = self._get_tracker_second_column_name()
        self._update_col_int_value(idx, col2_name, old_val)
        return old_val

    # ----------------------------------------------------------------------
    # Add a new column and return its name
    # ----------------------------------------------------------------------
    def _get_tracker_new_column_name(self, idx):
        new_col_inx = self._add_tracker_new_colum_inx(idx)
        return self._build_column_name(new_col_inx)

    # ----------------------------------------------------------------------
    # Delete a column from the table
    # ----------------------------------------------------------------------
    def _delete_column(self, idx: str, col_name: str):
        if not self.tarcker_table:
            self.glogger.error("This table (%s) is not extendable. Cannot delete the colum %s", self.table_name, col_name)
            return False
        if not self._column_exists(col_name):
            self.glogger.error("Trying to delet column %s from table %s. But the column does not exist", col_name, self.table_name)
            return False
        command = "DELETE " + col_name + " FROM " + self.table_name + " WHERE " + self.index_value + " = '" + str(idx) + "'"
        return self._execute_db_command(command)
        #TBD: Do we need to update the tracker ??????

    # ----------------------------------------------------------------------
    # Check if a column (by name) exists
    # ----------------------------------------------------------------------
    def _column_exists(self, col_name: str) -> bool:
        col_names = self.get_column_names()
        if col_name in col_names:
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    # Calculate the next column name
    # ----------------------------------------------------------------------
    def _next_column_index(self) -> int:
        next_col_inx = 1  # In case that the list is empty, return 1
        col_names = self.get_column_names()
        for col_name in col_names:
            if not col_name.startswith('_'):
                #print(col_name + " not started with _")
                continue
            number = col_name[1:]
            if not number.isnumeric():
                #print(col_name + " not numeric")
                continue
            temp_number = int(number)
            if temp_number < next_col_inx:
                #print(col_name + " next=" + str(temp_number) + " temp=" + str(next_col_inx))
                continue
            next_col_inx = temp_number + 1
        self.glogger.debug("The next column index to be created: %d", next_col_inx)
        #print(next_col_inx)
        return next_col_inx

    # ----------------------------------------------------------------------
    # Format the rows as single scalar of INT type
    # ----------------------------------------------------------------------
    def _format_row_as_single_int_scalar(self, rows):
        if not rows:
            return -1
        for row in rows:
            value = row[0]  # return the single scalar
            if not value:
                return -1
            #print(value)
            return int(value)

    # ----------------------------------------------------------------------
    # Format the rows as single scalar of the string type
    # ----------------------------------------------------------------------
    def _format_row_as_single_string_scalar(self, rows):
        if not rows:
            return None
        for row in rows:
            value = row[0]  # return the single scalar
            return value # Don't convert to string - return as is

    # ----------------------------------------------------------------------
    # Convert a single Row to dictionary
    # Row is of type: : cassandra.io.asyncorereactor.Row
    # ----------------------------------------------------------------------
    def _convert_single_row_to_dict(self, row , column_names : list) -> dict:
        if len(row) != len(column_names):
            self.glogger.error("The number of columns (%d) is not as the number of elements in the row: %d", len(column_names), len(row))
            return None
        rec = {}
        for inx, col in enumerate(row):
            if not col:
                continue
            rec[column_names[inx]] = str(col)
            #print(rec)
        self.glogger.debug("row=%s len(row)=%d type(row)=%s rec=%s", row, len(row), type(row), rec)
        return rec

    # ----------------------------------------------------------------------
    # Convert a single Row to a list of values
    # Row is of type: : cassandra.io.asyncorereactor.Row
    # ----------------------------------------------------------------------
    def _convert_single_row_to_list(self, row , all_column_names:list, column_names : list) -> list:
        #if len(row) != len(column_names):
        #    self.glogger.error("The number of columns (%d) is not as the number of elements in the row: %d", len(column_names), len(row))
        #    return None
        lst = [None] * len(column_names)
        #lst = list()
        #print(column_names)
        for inx, col in enumerate(row):
            colname = all_column_names[inx]
            #print(colname)
            colinx = column_names.index(colname) if colname in column_names else -1
            if colinx == -1:
                continue
            lst[colinx] = str(col)
            #if not colname in column_names:
            #    continue
            #lst.append(str(col))
            #print(lst)
        self.glogger.debug("row=%s len(row)=%d type(row)=%s lst=%s", row, len(row), type(row), lst)
        return lst

    # ----------------------------------------------------------------------
    # Convert the rows into a list of dictionaries
    # ----------------------------------------------------------------------
    def _convert_rows_to_dict_list(self, rows) -> list:
        rows_list = list()
        if not rows:
            self.glogger.debug("rows is empty - nothing to convert")
            return rows_list
        column_names = rows.column_names
        for row in rows:
            rec = self._convert_single_row_to_dict(row, column_names)
            if not rec:
                continue
            rows_list.append(rec)
        self.glogger.debug("rows=%s rows_list=%s", rows, rows_list)
        return rows_list

    # ----------------------------------------------------------------------
    # Convert the rows into a list of values, per column names
    # ----------------------------------------------------------------------
    def _convert_rows_to_value_list_per_colnames(self, rows, column_names : list) -> list:
        rows_list = list()
        if not rows:
            self.glogger.debug("rows is empty - nothing to convert")
            return rows_list
        for row in rows:
            lst = self._convert_single_row_to_list(row, rows.column_names, column_names)
            if not lst:
                continue
            rows_list.append(lst)
        self.glogger.debug("rows=%s rows_list=%s", rows, rows_list)
        return rows_list

    # ----------------------------------------------------------------------
    # Convert the rows into a list of values
    # ----------------------------------------------------------------------
    def _convert_rows_to_value_list(self, rows) -> list:
        return self._convert_rows_to_value_list_per_colnames(rows, rows.column_names)
        #rows_list = list()
        #if not rows:
        #    self.glogger.info("rows is empty - nothing to convert")
        #    return rows_list
        #column_names = rows.column_names
        #for row in rows:
        #    lst = self._convert_single_row_to_list(row, column_names)
        #    if not lst:
        #        continue
        #    rows_list.append(lst)
        #self.glogger.debug("rows=%s rows_list=%s", rows, rows_list)
        #return rows_list

# --------------------------------------------------------------------
# Create A extendable Table (adding more columns in run time)
# --------------------------------------------------------------------
def dbtable_create_table(table_name:str, prim_col_name="idx")  -> DbTable :
    columns_info = [(prim_col_name, "text PRIMARY KEY")]
    dbtable = DbTable(table_name, columns_info, is_extendable=False)
    return dbtable

# --------------------------------------------------------------------
# Delete a table
# --------------------------------------------------------------------
def dbtable_delete_table(table_name : str):
    dbtable = DbTable(table_name, None, is_extendable=False)
    dbtable.drop_table()

