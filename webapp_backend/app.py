import sys
import uuid
import datetime
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from flask_cors import CORS, cross_origin
from flask import jsonify
import msal
import app_config
import db_config

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from os import path

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey


#---------------------------------------------
# Create Logger
#---------------------------------------------
log = None
def _create_log():
    global log
    log = logging.getLogger("webapp_backend")
    log.setLevel("INFO")
    file_name="webapp_backend.txt"
    home = str(Path.home())
    log_fname = path.join(home, file_name)
    file_handler = TimedRotatingFileHandler(log_fname, when='midnight')
    FORMATTER = logging.Formatter("%(asctime)s-%(name)s-%(funcName)s-%(lineno)d-%(levelname)s- %(message)s")
    file_handler.setFormatter(FORMATTER)
    log.addHandler(file_handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    log.addHandler(console_handler)
    log.info("webapp_backend Started")

#---------------------------------------------
# Create Database
#---------------------------------------------
dbcontainer = None
def _create_db():
    global dbcontainer
    HOST = db_config.settings['host']
    MASTER_KEY = db_config.settings['master_key']
    DATABASE_ID = db_config.settings['database_id']
    CONTAINER_ID = db_config.settings['container_id']
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db = client.get_database_client(DATABASE_ID)
    dbcontainer = db.get_container_client(CONTAINER_ID)

#---------------------------------------------
# Validate Data
#---------------------------------------------
def _validateRegistrationData(data):
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

#------------------------------------------------------------
# Create a user in the database
#------------------------------------------------------------
def create_db_user(data):
    global dbcontainer
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
      dbcontainer.create_item(body=next_user)
      read_item = dbcontainer.read_item(item=data['username'], partition_key='User')
      log.info("Added the following to the db: %s", str(read_item))
      return { "isSuccess": isSuccess, "item": read_item }
    except exceptions.CosmosResourceExistsError as e:
      log.error("Exception in adding data=%s to the db err=%s", str(next_user), e)
      isSuccess = False
      error = str(e)
      if e.reason:
        error = e.reason
      return { "error": error, "isSuccess": isSuccess }
    except Exception as e:
      isSuccess = False
      error = str(e)
      log.error("Exception in adding data=%s to the db err=%s", str(next_user), e)
      return { "error": error, "isSuccess": isSuccess }

#------------------------------------------------------------
# Add user to Active Directory
#------------------------------------------------------------
def _add_user_to_activedir(data):
    result = {}
    errors = []
    try:
        token = None
        token_response = _get_admin_login_response()
        print(type(token_response))
        print(token_response)
        log.info("get_admin_login_response returned %s", str(token_response))
        if token_response and token_response["isSuccess"] and 'access_token' in token_response['result']:
          token = token_response['result']['access_token']
          log.info("Authentication succeeded")
        else:
          log.error("Authentication Failed")
          return {"errors": ['Authentication Failed'], "isSuccess": False}
    except Exception as err:
        log.error("failed to add the user to the active directory - Continue anyway. err=%s", err)
        return {"errors": ['get_admin_login_response Failed'], "isSuccess": False}

    mailNickname = data['username']
    upn = mailNickname + domainName

    userData = {
      "accountEnabled": True,
      "displayName": data['firstName'] + ' ' + data['lastName'],
      "mailNickname": mailNickname,
      "userPrincipalName": upn,
      "passwordProfile": {
        "forceChangePasswordNextSignIn": False,
        "password": data["password"]
      }}
    try:
        errors = []
        graph_data = requests.post(ms_graph_users_api,json=userData, headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
        print(type(graph_data))
        print(graph_data)
        if graph_data and 'error' in graph_data and 'message' in graph_data['error']:
            isSuccess = False
            errors.append('Azure Create User: ' + graph_data['error']['message'])
            log.error("Azure Create User Error=%s", str(errors))
            return jsonify({"errors": errors, "isSuccess": False})
        else:
            current_users += 1
            result = {"isSuccess": True}
            return result
    except Exception as err:
        log.error("failed to add the user to the active directory - Continue anyway. err=%s", err)
        return {"error": "Exception in requests.post", "isSuccess": False}

#------------------------------------------------------------
# Get login response
#------------------------------------------------------------
def _get_admin_login_response():
    log.info('get_admin_login_response_func begins')
    isSuccess = True
    username = app_config.ADMIN_USERNAME
    password = app_config.ADMIN_PASSWORD

    cache = _load_cache()
    x = msal.ConfidentialClientApplication(
          app_config.CLIENT_ID, authority=app_config.AUTHORITY,
          client_credential=app_config.CLIENT_SECRET, token_cache=cache
    )
    account = x.get_accounts(username=username)
    log.info('account: %s', str(account))
    result = None

    if len(account) == 0:
        try:
            result = x.acquire_token_by_username_password(username, password, app_config.SCOPE)
            _save_cache(cache)
        except Exception as e:
            isSuccess = False
            log.error("acquire_token_by_username_password failed err=%s", e)
            result = { "errors": [str(e)], "isSuccess": isSuccess }
            print(result, "------------------->")
            print(type(result), "------------------->")
            return result
    else:
        result = x.acquire_token_silent(app_config.SCOPE, account=account[0])

    if 'error' in result:
        log.error("get_admin_login_response failed result=%s", str(result))
        isSuccess = False

    return { "result": str(result), "isSuccess": isSuccess }


#------------------------------------------------------------
# Add user to database
#------------------------------------------------------------
def _add_user_to_db(data):
    create_user_response = create_db_user(data)
    if create_user_response and not create_user_response["isSuccess"]:
      suffix = ''
      if 'error' in create_user_response and create_user_response['error']:
        suffix = ': ' + create_user_response['error']
        log.error("Failed to create the user in the DB Erros=%s", str(suffix))
        return {"errors": ['Create DB User Failed' + suffix], "isSuccess": False}

    result = {"isSuccess": True, 'data': create_user_response['item']}
    return result

#------------------------------------------------------------
# Do initilizations
#------------------------------------------------------------
_create_log()
_create_db()
app = Flask(__name__)
app.config.from_object(app_config)
#cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)


ms_graph_users_api = "https://graph.microsoft.com/v1.0/users"
domainName = "@sprvargmail.onmicrosoft.com"
max_users = 20
current_users = 0


@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = _build_auth_code_flow(scopes=app_config.SCOPE)
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        ).json()
    return render_template('display.html', result=graph_data)

#-------------------------------------
# Register a user
#-------------------------------------
@app.route("/api/registration", methods=["post"])
@cross_origin()
def registration():
    log.info("Registration API called")
    isSuccess = True

    global max_users
    global current_users
    if current_users >= max_users:
        log.error("Max number of users excceded - allowd=%d exist=%d", max_users, current_users)
        return jsonify({ "errors": ['Custom Validation: Max Allowed Acounts'], "isSuccess": False })

    data = request.get_json()
    log.info("Registration data=%s", str(data))

    (isDataOk, validation_errors) = _validateRegistrationData(data)

    if not isDataOk:
      _errors = []
      _errors.extend(validation_errors)
      log.error("Registration Failed Erros=%s", str(_errors))
      return jsonify({ "errors": _errors, "isSuccess": False })

    data['username'] = str(data['username']).lower()

    result = _add_user_to_activedir(data)
    if isSuccess:
      log.info("Registration succeeded")
      jsonify({ "result": "Registration succeeded", "isSuccess": isSuccess }) # Add return
    else:
      log.error("Registration Failed Erros=%s", str(errors))
      jsonify({ "errors": errors, "isSuccess": isSuccess }) # Add return

    result = _add_user_to_db(data)
    isSuccess = result["isSuccess"]
    if isSuccess:
      log.info("DB update succeeded")
      return jsonify({ "result": "DB update succeeded", "isSuccess": isSuccess })
    else:
      log.error("DB Update Failed")
      return jsonify({ "isSuccess": isSuccess })

#-------------------------------------
# Load Cache
#-------------------------------------
def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

#-------------------------------------
# Save Cache
#-------------------------------------
def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)

def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=url_for("authorized", _external=True))

def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result

app.jinja_env.globals.update(_build_auth_code_flow=_build_auth_code_flow)  # Used in template

if __name__ == "__main__":
    app.run()

