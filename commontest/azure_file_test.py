from common.models.azure_file_strage import *

azfileclient = AzureFileStorage.get_instance()
filename = "C:\\Users\\Danny\\Downloads\\20220817_105300.jpg"
azfileclient.upload_contract(filename)
azfileclient.list_contracts()
azfileclient.download_contract("20220817_105300.jpg")
azfileclient.delete_contract("20220817_105300.jpg")
