import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config

from flask import jsonify
import logging
from flask_cors import CORS, cross_origin


import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime

import db_config


HOST = db_config.settings['host']
MASTER_KEY = db_config.settings['master_key']
DATABASE_ID = db_config.settings['database_id']
CONTAINER_ID = db_config.settings['container_id']


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

##
max_users = 20
current_users = 0
##

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
db = client.get_database_client(DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)


# from werkzeug.middleware.proxy_fix import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

ms_graph_users_api = "https://graph.microsoft.com/v1.0/users"
domainName = "@sprvargmail.onmicrosoft.com"

# @app.route("/")
# def index():
#     if not session.get("user"):
#         return redirect(url_for("login"))
#     return render_template('index.html', user=session["user"], version=msal.__version__)


@app.route("/api/registration", methods=["post"])
@cross_origin()
def registration():
  isSuccess = True

  global current_users
  if max_users >= current_users:
    jsonify({ "errors": ['Custom Validation: Max Allowed Acounts'], "isSuccess": False })

  data = request.get_json()

  (isDataOk, validation_errors) = validateRegistrationData(data)

  if not isDataOk:
    _errors = []
    _errors.extend(validation_errors)
    return jsonify({ "errors": _errors, "isSuccess": False })

  data['username'] = str(data['username']).lower()

  token = None
  token_response = get_admin_login_response()
  if token_response and token_response["isSuccess"] and 'access_token' in token_response['result']:
    token = token_response['result']['access_token']
  else:
    return jsonify({ "errors": ['Authentication Failed'], "isSuccess": False })

  result = {}
  errors = []

  mailNickname = data['username']
  upn = mailNickname + domainName

  userData = {
    "accountEnabled": True,
    "displayName": data['firstName'] + ' ' + data['lastName'],
    "mailNickname": mailNickname,
    "userPrincipalName": upn,
    "passwordProfile" : {
      "forceChangePasswordNextSignIn": False,
      "password": data["password"]
  }}
  graph_data = requests.post(
    ms_graph_users_api,
    json = userData,
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}).json()
  if graph_data and 'error' in graph_data and 'message' in graph_data['error']:
    isSuccess = False
    errors.append('Azure Create User: ' + graph_data['error']['message'])
  else:
    current_users += 1
    result = {
      **result,
      'graphData': graph_data
    }

    create_user_response = create_db_user(data)
    if create_user_response and not create_user_response["isSuccess"]:
      suffix = ''
      if 'error' in create_user_response and create_user_response['error']:
        suffix = ': ' + create_user_response['error']
        return jsonify({ "errors": ['Create DB User Failed' + suffix], "isSuccess": False })

    result = {
      **result,
      'data': create_user_response['item']
    }


  if isSuccess:
    return jsonify({ "result": result, "isSuccess": isSuccess })
  else:
    return jsonify({ "errors": errors, "isSuccess": isSuccess })


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

# def update_db_user_with_azure_success(username):
#   isSuccess = True
#   try:
#     read_item = container.read_item(item=username, partition_key='User')
#     next_value = {
#     **read_item,
#       "azureADCreated": True,
#       "azureADCreatedAT": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
#     }
#     response = container.upsert_item(body=next_value)
#     return { "result": response, "isSuccess": isSuccess }
#   except Exception as e:
#     isSuccess = False
#     return { "error": str(e), "isSuccess": isSuccess }

def create_db_user(data):
  isSuccess = True
  baseInfo = {
    'id': data['username'],
    'partitionKey': 'User',
    'firstName': data['firstName'],
    'lastName': data['lastName'],
    'email': data['email'],
    'finra': data['finra'],
    'phone': data['phone'],
  }

  address = {
    "name": data['address']['name'],
    "details": data['address']['details'],
    "city": data['address']['city'],
    "state": data['address']['state'],
    "zipCode": data['address']['zipCode'],
  }

  next_user = {
    **baseInfo,
    'address': address,
    "upn": data['username'] + domainName,
    "createdAt": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
    'isCompany': data['isCompany'],
  }

  try:
    container.create_item(body=next_user)
    read_item = container.read_item(item=data['username'], partition_key='User')
    return { "isSuccess": isSuccess, "item": read_item }
  except exceptions.CosmosResourceExistsError as e:
    isSuccess = False
    error = str(e)

    if e.reason:
      error = e.reason
    return { "error": error, "isSuccess": isSuccess }
  except Exception as e:
    isSuccess = False
    error = str(e)
    return { "error": error, "isSuccess": isSuccess }


def validateRegistrationData(data):
  result = None
  errors = []

  hasFirstName = 'firstName' in data and data['firstName']
  hasLastName = 'lastName' in data and data['lastName']

  hasFinra = 'finra' in data and data['finra']
  hasPhone = 'phone' in data and data['phone']
  hasEmail = 'email' in data and data['email']
  hasUsername = 'username' in data and data['username']
  hasPassWord = 'password' in data and data['password']

  hasAddress = 'address' in data and data['address']
  hasAddressName = hasAddress and 'name' in data['address'] and data['address']['name']
  hasAddressCity = hasAddress and 'city' in data['address'] and data['address']['city']
  hasAddressState = hasAddress and 'state' in data['address'] and data['address']['state']
  hasAddressZipcode = hasAddress and 'zipCode' in data['address'] and data['address']['zipCode']

  hasIsCompany = 'isCompany' in data

  result = (
    hasFirstName and
    hasLastName and
    hasFinra and
    hasPhone and
    hasEmail and
    hasUsername and
    hasPassWord and
    hasAddress and
    hasAddressName and
    hasAddressCity and
    hasAddressState and
    hasAddressZipcode and hasIsCompany)

  if not hasFirstName:
    errors.append('First name is mandatory!')
  if not hasLastName:
    errors.append('Last name is mandatory!')
  if not hasFinra:
    errors.append('Finra is mandatory!')

  if not hasPhone:
    errors.append('Phone is mandatory!')
  if not hasEmail:
    errors.append('Email is mandatory!')
  if not hasUsername:
    errors.append('Username is mandatory!')
  if not hasPassWord:
    errors.append('Password is mandatory!')

  if not hasAddress:
    errors.append('Address fields are mandatory!')
  if hasAddress and not hasAddressName:
    errors.append('Address, Name is mandatory!')
  if hasAddress and not hasAddressCity:
    errors.append('Address, City is mandatory!')
  if hasAddress and not hasAddressState:
    errors.append('Address, State is mandatory!')
  if hasAddress and not hasAddressZipcode:
    errors.append('Address, Zipcode is mandatory!')

  if not hasIsCompany:
    errors.append('IsCompany field is mandatory!')

  return (result, errors)


def get_admin_login_response():
  # print('get_admin_login_response_func begins ---------->')
  isSuccess = True
  username = app_config.ADMIN_USERNAME
  password = app_config.ADMIN_PASSWORD


  cache = _load_cache()
  x = msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache
  )
  account = x.get_accounts(username=username)
  # print('account ---------->', account)
  result = None

  if len(account) == 0:
    try:
      result = x.acquire_token_by_username_password(username, password, app_config.SCOPE)
      _save_cache(cache)
    except Exception as e:
      isSuccess = False
      return jsonify({ "errors": [str(e)], "isSuccess": isSuccess })
  else:
    result = x.acquire_token_silent(app_config.SCOPE, account=account[0])

    if 'error' in result: isSuccess = False

  return { "result": result, "isSuccess": isSuccess }

# def init_db():
#     client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
#     try:
#         # setup database for this sample
#         try:
#             print('create db .....')
#             db = client.create_database(id=DATABASE_ID)
#             print('Database with id \'{0}\' created'.format(DATABASE_ID))
#
#         except exceptions.CosmosResourceExistsError:
#             print('get db .....')
#             db = client.get_database_client(DATABASE_ID)
#             print('Database with id \'{0}\' was found'.format(DATABASE_ID))
#
#         # setup container for this sample
#         try:
#             container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/partitionKey'))
#             # container = db.create_container(id=CONTAINER_ID)
#             print('Container with id \'{0}\' created'.format(CONTAINER_ID))
#
#         except exceptions.CosmosResourceExistsError:
#             container = db.get_container_client(CONTAINER_ID)
#             print('Container with id \'{0}\' was found'.format(CONTAINER_ID))
#
#     except exceptions.CosmosHttpResponseError as e:
#         print('\nrun_sample has caught an error. {0}'.format(e.message))
#
#     finally:
#             print("\nrun_sample done")

if __name__ == "__main__":
    app.run()

# init_db()
