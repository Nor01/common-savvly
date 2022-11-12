from database.db_wrapper import CosmosFactory
import os

from database.db_tablecollection import DbTableCollection
from database.db_user_data import UserData

if __name__ == '__main__':

    d = UserData()
    print(d.get_tables_info())