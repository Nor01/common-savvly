import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://savvly.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'cBl5HjpCQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'SavvlyDB'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'User'),
}
