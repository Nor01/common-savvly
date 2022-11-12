import os

CLIENT_ID = "4f484def-7f3f-4ee0-ab1a-6f6427ee6fc3" # Application (client) ID of app registration
CLIENT_SECRET = "cCN8Q~wrWWkhwnm.uVFE_Pg7RnsgFn2rzaGInchH" # Placeholder - for use ONLY during testing.
AUTHORITY = "https://login.microsoftonline.com/3e1414dc-cb91-42fe-8f78-976df10b4ebe"  # For multi-tenant app
REDIRECT_PATH = "/getAToken"
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent
SCOPE = ["User.ReadBasic.All"]
SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
ADMIN_USERNAME = ''
ADMIN_PASSWORD = ''

#CLIENT_ID = "4f484def-7f3f-4ee0-ab1a-6f6427ee6fc3"
#CLIENT_SECRET = "cCN8Q~wrWWkhwnm.uVFE_Pg7RnsgFn2rzaGInchH"
#AUTHORITY = "https://login.microsoftonline.com/3e1414dc-cb91-42fe-8f78-976df10b4ebe"
##ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
#SCOPE = ["Directory.ReadWrite.All", "User.ReadWrite.All"]
##SESSION_TYPE = "filesystem"
#ADMIN_USERNAME = ''
#ADMIN_PASSWORD = ''

#CLIENT_ID = "8e"
#CLIENT_SECRET = "qTr"
#AUTHORITY = "https://login.microsoftonline.com/a71d0"
#ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
#SCOPE = ["Directory.ReadWrite.All", "User.ReadWrite.All"]
#SESSION_TYPE = "filesystem"
#ADMIN_USERNAME = ''
#ADMIN_PASSWORD = ''
