from azure_ad_verify_token import verify_jwt


azure_ad_app_id = 'e41831ff-9f6c-466d-bb12-e1f39cba16b8'
azure_ad_issuer = 'https://savvlyb2c.b2clogin.com/7d9e372e-1567-4212-8abb-f5395ba779f7/v2.0/'
azure_ad_jwks_uri = 'https://savvlyb2c.b2clogin.com/savvlyb2c.onmicrosoft.com/B2C_1_Savvly_signin/discovery/v2.0/keys'

accessToken="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsifQ.eyJpc3MiOiJodHRwczovL3NhdnZseWIyYy5iMmNsb2dpbi5jb20vN2Q5ZTM3MmUtMTU2Ny00MjEyLThhYmItZjUzOTViYTc3OWY3L3YyLjAvIiwiZXhwIjoxNjU3MjE3MTc1LCJuYmYiOjE2NTcyMTM1NzUsImF1ZCI6ImU0MTgzMWZmLTlmNmMtNDY2ZC1iYjEyLWUxZjM5Y2JhMTZiOCIsIm9pZCI6Ijc2M2QyMjZhLTdlOGQtNGQ0Ny04YjJkLWE5NmZjNjQ4OTlmZiIsInN1YiI6Ijc2M2QyMjZhLTdlOGQtNGQ0Ny04YjJkLWE5NmZjNjQ4OTlmZiIsIm5hbWUiOiJ1bmtub3duIiwiZ2l2ZW5fbmFtZSI6IkRhbkRhbiIsInN0YXRlIjoiQUwiLCJmYW1pbHlfbmFtZSI6IlphZG9rIiwiZXh0ZW5zaW9uX2NyZF9udW1iZXIiOiIxMjM0NTY3OCIsImV4dGVuc2lvbl9QaG9uZU51bWJlciI6IjEyMzQ1Njc4OTAiLCJlbWFpbHMiOlsiZGFuZGFuLnphZG9rQGdtYWlsLmNvbSJdLCJ0ZnAiOiJCMkNfMV9TYXZ2bHlfc2lnbmluIiwibm9uY2UiOiI4ZjQ0YWRkMi1jYzBmLTQ0N2UtOTk0ZC1kMGVkN2ZkY2QyYTQiLCJhenAiOiJlNDE4MzFmZi05ZjZjLTQ2NmQtYmIxMi1lMWYzOWNiYTE2YjgiLCJ2ZXIiOiIxLjAiLCJpYXQiOjE2NTcyMTM1NzV9.oE2YucrXjzAd8C8f1VjIxTpJ5aauqABGU4MGVmjZ228FQAmTnbWYSqMHb7U8vIpK15-uXaO09fJ5TeF_eZyHGO_M-aZ10lFpZDl7rLEf3OhmWRjKa21PS2fwwTENDkiQhTTr0q6zqVFa2OIHUEPw-L06ajv2MbeJlhjVkgclMMcTo0zDOsIbPmaCmD54u2qKQfZkvEFkL17VMbd0iXNQav5K_WMBHPx6td-VmBga3bT9GM_QsJwL7Lf2021lDEIV4rzTnPYynUXrSDZrE9WuUeiJISs6K_LMou7ubpTYipxuM8R4Zrx3XlfRVGeA7IXd4eXk7Rhd7h4mcww57TKq1g"

payload = verify_jwt(
    token=accessToken,
    valid_audiences=[azure_ad_app_id],
    issuer=azure_ad_issuer,
    jwks_uri=azure_ad_jwks_uri,
    verify=True,
)

print(payload)


#import msal
##import jwt
##import json
#import requests
#import pandas as pd
#from datetime import datetime

#  import jwt
#  key = "secret"
#  encoded = jwt.encode({"some": "payload"}, key, algorithm="HS256")
#  print(encoded)
#  #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
#  decoded = jwt.decode(encoded, key, algorithms="HS256")
#  print(decoded)
#  #{'some': 'payload'}

##accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsifQ.eyJpc3MiOiJodHRwczovL3NhdnZseWIyYy5iMmNsb2dpbi5jb20vN2Q5ZTM3MmUtMTU2Ny00MjEyLThhYmItZjUzOTViYTc3OWY3L3YyLjAvIiwiZXhwIjoxNjU3MTI1NDQ4LCJuYmYiOjE2NTcxMjE4NDgsImF1ZCI6IjA5ODRlMTY1LTYyNzAtNGNhZi1iNWExLTA2MTI0Y2ExMjNmMCIsIm9pZCI6IjdiMWJiMjNlLTEyY2MtNDRjNy05NzA2LTFjYmNhYzMwZjZlZSIsInN1YiI6IjdiMWJiMjNlLTEyY2MtNDRjNy05NzA2LTFjYmNhYzMwZjZlZSIsIm5hbWUiOiJ1bmtub3duIiwiZ2l2ZW5fbmFtZSI6IldpbGwiLCJzdGF0ZSI6IlRYIiwiZmFtaWx5X25hbWUiOiJQYWl6IiwiZXh0ZW5zaW9uX2NvbXBhbnlfY3JkX251bWJlciI6IldGMTIzNCIsImV4dGVuc2lvbl9jb21wYW55X25hbWUiOiJXaWxsXHUwMDI3cyBGaXJtIiwiZXh0ZW5zaW9uX2NvbXBhbnlfdHlwZSI6ZmFsc2UsImV4dGVuc2lvbl9jcmRfbnVtYmVyIjoiQUJDRDEyMzQiLCJleHRlbnNpb25fUGhvbmVOdW1iZXIiOiI5OTkxNjgzNiIsImVtYWlscyI6WyJ3YXdhbTQ4NzA4QGhla2Fycm8uY29tIl0sInRmcCI6IkIyQ18xX1NhdnZseV9zaWduaW4iLCJub25jZSI6ImU5ZTMwMTYyLTRiMmEtNDkwYy05ZGExLTUzMmJmM2EzNjc3NiIsImF6cCI6IjA5ODRlMTY1LTYyNzAtNGNhZi1iNWExLTA2MTI0Y2ExMjNmMCIsInZlciI6IjEuMCIsImlhdCI6MTY1NzEyMTg0OH0.PQWd7iWVSeFcng_DRQ-6jFGLFipIVqnWxRXzWIXKkxXmvcTci4yxYHxI1LnZeuZlfyChKLMgXSstxYviedTy9we923k98AMG-Tryy9_cL1246L0M8FzNVVK7WbMo6fpPVPNRsljuWbFKFeNoYqTYxBZXsgBr-X-WOOSPYCIRpnUeso78u6Yd5TaanLGVnXwWQVsSq3WhtdwDskhypl-RELk5RGH7hzaGqG4As6nXN-i5xniB_9eoQnpkABJu1F8cNUvRM4aH4tEgc7eQOVOW-DetDqyOj7Dm3Dv7i20rLM7v3IjuGgJRKqxUfblfBEPskOQ_8yfidr4udDKEF4mhiQ"
##decodedAccessToken = jwt.decode(accessToken, verofy=False, algorithms=["HS256", "RS256"])
##accessTokenFormatted = json.dumps(decodedAccessToken, indent=2)
##print('Decoded Access Token')
##print(accessTokenFormatted)


#from flask_pyjwt import AuthManager, current_token, require_token
#
#
#def test_token():
#    token_type = "auth"
#    location = "header"
#    #auth_header = request.headers.get("Authorization")
#    auth_header = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsifQ.eyJpc3MiOiJodHRwczovL3NhdnZseWIyYy5iMmNsb2dpbi5jb20vN2Q5ZTM3MmUtMTU2Ny00MjEyLThhYmItZjUzOTViYTc3OWY3L3YyLjAvIiwiZXhwIjoxNjU3MTI1NDQ4LCJuYmYiOjE2NTcxMjE4NDgsImF1ZCI6IjA5ODRlMTY1LTYyNzAtNGNhZi1iNWExLTA2MTI0Y2ExMjNmMCIsIm9pZCI6IjdiMWJiMjNlLTEyY2MtNDRjNy05NzA2LTFjYmNhYzMwZjZlZSIsInN1YiI6IjdiMWJiMjNlLTEyY2MtNDRjNy05NzA2LTFjYmNhYzMwZjZlZSIsIm5hbWUiOiJ1bmtub3duIiwiZ2l2ZW5fbmFtZSI6IldpbGwiLCJzdGF0ZSI6IlRYIiwiZmFtaWx5X25hbWUiOiJQYWl6IiwiZXh0ZW5zaW9uX2NvbXBhbnlfY3JkX251bWJlciI6IldGMTIzNCIsImV4dGVuc2lvbl9jb21wYW55X25hbWUiOiJXaWxsXHUwMDI3cyBGaXJtIiwiZXh0ZW5zaW9uX2NvbXBhbnlfdHlwZSI6ZmFsc2UsImV4dGVuc2lvbl9jcmRfbnVtYmVyIjoiQUJDRDEyMzQiLCJleHRlbnNpb25fUGhvbmVOdW1iZXIiOiI5OTkxNjgzNiIsImVtYWlscyI6WyJ3YXdhbTQ4NzA4QGhla2Fycm8uY29tIl0sInRmcCI6IkIyQ18xX1NhdnZseV9zaWduaW4iLCJub25jZSI6ImU5ZTMwMTYyLTRiMmEtNDkwYy05ZGExLTUzMmJmM2EzNjc3NiIsImF6cCI6IjA5ODRlMTY1LTYyNzAtNGNhZi1iNWExLTA2MTI0Y2ExMjNmMCIsInZlciI6IjEuMCIsImlhdCI6MTY1NzEyMTg0OH0.PQWd7iWVSeFcng_DRQ-6jFGLFipIVqnWxRXzWIXKkxXmvcTci4yxYHxI1LnZeuZlfyChKLMgXSstxYviedTy9we923k98AMG-Tryy9_cL1246L0M8FzNVVK7WbMo6fpPVPNRsljuWbFKFeNoYqTYxBZXsgBr-X-WOOSPYCIRpnUeso78u6Yd5TaanLGVnXwWQVsSq3WhtdwDskhypl-RELk5RGH7hzaGqG4As6nXN-i5xniB_9eoQnpkABJu1F8cNUvRM4aH4tEgc7eQOVOW-DetDqyOj7Dm3Dv7i20rLM7v3IjuGgJRKqxUfblfBEPskOQ_8yfidr4udDKEF4mhiQ"
#    if not auth_header or not is_valid_auth_header(auth_header):
#        print("Improperly formatted or missing Authorization header")
#        return
#    jwt_token = auth_header[7:]
#    auth_manager: AuthManager = current_app.auth_manager
#    is_valid_token = auth_manager.verify_token(jwt_token)
#    if not is_valid_token:
#        print(f"{token_type} token is not valid")
#        return
#    jwt = auth_manager.convert_token(jwt_token)
#    if jwt.token_type != TokenType[token_type.upper()]:
#        print(f"Invalid token type of {jwt.token_type}")
#        return
#    print("OK")
#    return