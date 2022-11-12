from flask_session.__init__ import Session
#from flask_cors import CORS, cross_origin
#from Flask import flask, request
#from flask_pyjwt import auth_manager, current_token, require_token
#from flask_pyjwt import current_token, require_token
#from flask_pyjwt import AuthManager, current_token, require_token
#from apscheduler.schedulers.background import BackgroundScheduler
#import atexit

from proxy.request_helper import *
from proxy.session import *

# ---------------------------------------------------------------------
# Create an instrance of the logger (This must be before our imports )
# ----------------------------------------------------------------------
#from common.util.utility_functions import utils_get_version
from common.util.logging_helper import get_logger
glogger = get_logger("api")
glogger.info("Savvly API Web Server started")

# ---------------------------------------------------------------------
# Load the configuration file
# ----------------------------------------------------------------------
from common.util.config_wrapper import config_wrapper_init
config_wrapper_init("common/")

# ---------------------------------------------------------------------
# Now, import our modules
# ----------------------------------------------------------------------
from housekeeper.housekeeper import housekeeper_init
#from proxy.proxy import proxy_run, proxy_set_response_header
from proxy.proxy import proxy_run
#from proxy.usertype import UserType
from auth.auth import *
#from common.msgraph.msgraphapp import msgraphapp_refresh_token

# -----------------------------------------------------------------------------------
# Setup up a Flask instance and support server-side sessions using Flask-Session
# -----------------------------------------------------------------------------------
app = Flask(__name__)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
app.config['SESSION_TYPE'] = 'filesystem'  # Specifies flask-sessions module that server-side sessions written to disk
app.config['SESSION_PERMANENT'] = False    # The session is not permanent
app.config['SECRET_KEY'] = os.urandom(32)  # Generate a random key to protect against CSRF
#app.config["JWT_ISSUER"] = "Flask_PyJWT" # Issuer of tokens
#app.config["JWT_AUTHTYPE"] = "HS256" # HS256, HS512, RS256, or RS512
#app.config["JWT_SECRET"] = "x_98Q~HwEufkGYfeZ2t~d7hV4GGvkPgofOQO0btX" # string for HS256/HS512, bytes (RSA Private Key) for RS256/RS512
#app.config["JWT_AUTHMAXAGE"] = 3600
#app.config["JWT_REFRESHMAXAGE"] = 604800
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
Session(app)

#auth_manager = AuthManager(app)

# ---------------------------------------------------------------------
# # Create the authentication object
# ----------------------------------------------------------------------
auth_init(Auth.auth_method_activedir, app)   # User Active Directory Authentication

# --------------------------------------------------------------------------------
# Initialize the house-keeper
# ---------------------------------------------------------------------------------
housekeeper_init()
#housekeeper_job_db_connect()              # Connect for the first time
#gscheduler = BackgroundScheduler(daemon=True, timezone="America/New_York")
#gscheduler.add_job(housekeeper_job_db_connect, 'interval', minutes=1)
#gscheduler.add_job(housekeeper_job_update_fmv, 'interval', minutes=6000)  # This is instead of FMV docker
#gscheduler.add_job(housekeeper_job_new_signed_contracts, 'interval', hours=1)  # Process the new sgned contracts
#gscheduler.add_job(housekeeper_job_sync_storage_contracts, 'interval', minutes=1)  # Sync the contracts on the storage
#gscheduler.add_job(housekeeper_job_upload_old_log_files, 'interval', hours=6)  # Upload the old log files to Azure
##gscheduler.add_job(msgraphapp_refresh_token, 'interval', minutes=45)  # Refresh MS-Graph Access Token
#gscheduler.start()
#atexit.register(lambda: gscheduler.shutdown())  # Shut down the scheduler when exiting the app

# -----------------------------------------------------------------------------------
# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
# -----------------------------------------------------------------------------------
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# --------------------------------------------------------------
# This function is called before each request by Flask
# --------------------------------------------------------------
@app.before_request
def before_request_func():
    glogger.debug("before_request executing!")

# --------------------------------------------------------------
# This function is called after each request by Flask
# --------------------------------------------------------------
@app.after_request
def after_request(response):
    #white_origin = ['https://savvly-dev-api.azurewebsites.net',
    #                'http://localhost:5000',
    #                'http://localhost:3000',
    #                'https://localhost:3000',
    #                'https://savvlyb2c.b2clogin.com',
    #                'http://localhost:8080']
    #if request.referrer:
    #    glogger.debug("request.referrer is: %s", request.referrer)
    #    host = request.referrer[:-1]
    #else:
    #    glogger.error("request.referrer is None. Cannot add headers")
    #    host =    'https://savvly-dev-api.azurewebsites.net' #'http://localhost:8080'
    #response.headers.add('Custom-Header', 'Danny Header')
    #response.headers['Origin'] = host
    #response.headers['Access-Control-Allow-Origin'] = '*'
    #response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    #response.set_cookie('some-cookie', value='some-cookie-value')
    # response.headers.add('Set-Cookie', f'session=%s; SameSite=None; Secure' % request_get_cookies())
    # response.headers.add("Access-Control-Allow-Origin", "*");
    # response.headers.add("Access-Control-Allow-Origin", "http://localhost:5000");
    # response.headers.add("Access-Control-Allow-Headers", "Authorization, Origin, X-Requested-With, Content-Type, Accept");
    #print("AFTER REQUEST-------------->>>>>>")
    #print(response.headers)
    glogger.debug("After Request - setting headers")
    response.headers.add('Content-Type', 'application/json')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    response.headers.add("Access-Control-Max-Age", "1440")
    return response

# --------------------------------------------------------------
# for health check
# Eliminate the annoying favicon.ico
# Eliminate the annoying robots933456.txt
# --------------------------------------------------------------
@app.route("/")
@app.route("/robots933456.txt")
@app.route("/favicon.ico")
def _ret_ok():
    return 'OK', 200

# ---------------------------------------------
# Post successfull Login
# ----------------------------------------------
#def _post_good_authentication():
#    glogger.debug("Authentication succeeded")
#    logged_user_id = auth_get_current_userid()
#    user_type = UserType.get_instance().get_user_type(logged_user_id)  # Find the user type and store in the session
#    session_set_user_type(user_type)
#    return proxy_run("loginok")

# ---------------------------------------------
# Post Authentication
# ----------------------------------------------
#def _post_authentication():
#    authenticated, redirect_url = auth_authenticate()
#    glogger.debug("After auth_authenticate. authenticated=%s redirect_url=%s", authenticated, redirect_url)
#    if authenticated:
#        glogger.debug("Calling _post_good_authentication")
#        return _post_good_authentication()
#    if redirect_url is None:
#        glogger.debug("Authentication failed")
#        return proxy_run("loginfail")
#    glogger.debug("redirect_url=%s", redirect_url)
#    result = redirect(redirect_url, code=302)
#    #result = proxy_set_response_header(result)
#    glogger.debug("Returning from _post_authentication")
#    return result

# ---------------------------------------------
# Login
# ----------------------------------------------
@app.route('/login')
#@cross_origin()
def login():
    url = auth_get_login_url()
    return redirect(url, code=302)
    #auth_start_login()   # Set the appropriate user-flow in the session (signin)
    #response = _post_authentication()
    #glogger.debug("Returning from login")
    #print(response.headers)
    #return response

# ---------------------------------------------
# Logout
# ----------------------------------------------
@app.route('/logout')
#@cross_origin()
def logout():
    # flask_login.logout_user()
    return proxy_run("logout")

# ---------------------------------------------
# Register/Signup a User
# ----------------------------------------------
@app.route('/registeruser')
#@cross_origin()
def registeruser():
    url = auth_get_register_user_url()
    return redirect(url, code=302)
    #auth_start_register_user()   # Set the appropriate user-flow in the session (signin)
    #return _post_authentication()

# ---------------------------------------------
# Register/Signup a RIA
# ----------------------------------------------
@app.route('/registerria')
#@cross_origin()
def registerria():
    url = auth_get_register_advisor_url()
    return redirect(url, code=302)
    #auth_start_register_ria()   # Set the appropriate user-flow in the session (signin)
    #return _post_authentication()

# ------------------------------------------------------------------------------------------------
# Authorized:  This is a Callback function that is called by the server after user authorization
# This callback function must be registered at the  server side
# ------------------------------------------------------------------------------------------------
@app.route('/getAToken')
def getAToken():
    #auth_start_login()
    #request_print()
    #session_print()
    #glogger.info("The callback getAToken() is called")
    if auth_check_result():
        return proxy_run("loginok")
    else:
        return proxy_run("loginfail")


# --------------------------------------------------------------
# A generic URL to handle multiple functions
# --------------------------------------------------------------
@app.route('/<funcname>', methods=['GET', 'POST'])
#@require_token()
def _route_to_func(funcname):
    glogger.debug("auth_header=%s", request.headers.get("Authorization"))
    result = proxy_run(funcname)
    return result

# --------------------------------------------------------------
# The program starts here
# --------------------------------------------------------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
