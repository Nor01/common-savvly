import os

import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://savvlydb-for-webapp-frontend.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'ZdX1sY30FGJKE0b2ep6CeNr9SgrAmpJpFxjtdFp3fafOp3bD56Ens7wD1avFqsezxKGmdlOWmR6kZzmyBwguMg=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'ToDoList'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Items'),
}

#settings = {
    #'host': os.environ.get('ACCOUNT_HOST', 'https://savvly.documents.azure.com:443/'),
    #'master_key': os.environ.get('ACCOUNT_KEY', 'cBl5HjpCQ=='),
    #'database_id': os.environ.get('COSMOS_DATABASE', 'SavvlyDB'),
    #'container_id': os.environ.get('COSMOS_CONTAINER', 'User'),
#}
