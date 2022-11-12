from pymongo import MongoClient
from dotenv import load_dotenv,find_dotenv
import os

load_dotenv(find_dotenv()) #instance the .env file to get the information

#===============================================
#===============MONGODB CONFIG==================
#===============================================

#Connection string with MONGODB
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://mainor:{password}@maincluster.ujttw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(connection_string)
dbs = client.list_database_names()
# print(dbs) #print all databases
