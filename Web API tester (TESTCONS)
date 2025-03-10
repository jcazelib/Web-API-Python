"""
Python script used for testing the available CP API endpoints in paper using TESTCONS - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#endpoints
For more information regarding TESTCONS please refer to - https://www.interactivebrokers.com/campus/ibkr-api-page/cpapi-v1/#testcons

This script assumes you've already received a Live Session Token & Access Token for TESTCONS
    Lines 21 - 23: Enter your consumer_key | access_token | live_session_token | (optional) accountId which is the U-account or DU-account number
"""

import json
import requests
import random
import base64
import pprint
from datetime import datetime
from urllib.parse import quote, quote_plus
from Crypto.Hash import SHA256, HMAC, SHA1

#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-INPUTS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-==---==
#==================================================================================================================
consumer_key = "TESTCONS"
access_token = "ACCESSTOKEN"
live_session_token = "LIVESESSIONTOKEN"
accountId = "ACCOUNTID"


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-SESSION-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-==---=
#==================================================================================================================
baseURL = 'api.ibkr.com'
bbody = []
replybody = []

method = 'GET'
url = f'https://{baseURL}/v1/api/portfolio/accounts'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/tickle'

# method = 'POST'                                                                
# url = f'https://{baseURL}/v1/api/iserver/auth/ssodh/init'
# body = {"publish":True, "compete":True}

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/accounts'

# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/auth/status'

# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/questions/suppress'
# bbody = {
#   "messageIds":["p12","o0"]
# }

# method = 'POST'
# url = f'https://{baseURL}/v1/api/logout'


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-OAuth 1.0a-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-===
#==================================================================================================================
session_object = requests.Session()
realm = "test_realm"

RESP_HEADERS_TO_PRINT = ["Content-Type", "Content-Length", "Date", "Set-Cookie", "User-Agent"]
print("")

def pretty_request_response(resp: requests.Response) -> str:
    """Print request and response legibly."""
    req = resp.request
    rqh = '\n'.join(f"{k}: {v}" for k, v in req.headers.items())
    rqh = rqh.replace(', ', ',\n    ')
    rqb = f"\n{pprint.pformat(json.loads(req.body))}\n" if req.body else ""
    try:
        rsb = f"\n{pprint.pformat(resp.json())}\n" if resp.text else ""
    except json.JSONDecodeError:
        rsb = resp.text
    rsh = '\n'.join([f"{k}: {v}" for k, v in resp.headers.items() if k in RESP_HEADERS_TO_PRINT])
    return_str = '\n'.join([
        #80*'-',
        '-----------REQUEST-----------',
        f"{req.method} {req.url}",
        "",
        rqh,
        f"{rqb}",
        "",
        '-----------RESPONSE-----------',
        f"{resp.status_code} {resp.reason}",
        rsh,
        f"{rsb}\n",
        "",
    ])
    return return_str


oauth_params = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": hex(random.getrandbits(128))[2:],
        "oauth_signature_method": "HMAC-SHA256",
        "oauth_timestamp": str(int(datetime.now().timestamp())),
        "oauth_token": access_token
    }


params_string = "&".join([f"{k}={v}" for k, v in sorted(oauth_params.items())])

base_string = f"{method}&{quote_plus(url)}&{quote(params_string)}"
encoded_base_string = base_string.encode("utf-8")


bytes_hmac_hash = HMAC.new(
    key=base64.b64decode(live_session_token), 
    msg=encoded_base_string,
    digestmod=SHA256
    ).digest()

b64_str_hmac_hash = base64.b64encode(bytes_hmac_hash).decode("utf-8")
oauth_params["oauth_signature"] = quote_plus(b64_str_hmac_hash)
oauth_params["realm"] = realm
oauth_header = "OAuth " + ", ".join([f'{k}="{v}"' for k, v in sorted(oauth_params.items())])
headers = {"Authorization": oauth_header}
headers["User-Agent"] = "python/3.11"

print("CONSUMER KEY = ", consumer_key)
print("")

#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-OAuth 1.0a sending the http request=-===-=-==-=-=-=-----=-=-=-=-==-=-=-=
#====================================================================================================================
#IF no JSON body & no replybody (i.e. for GET requests)
if len(bbody) == 0 and len(replybody) == 0:
    accounts_request = requests.Request(method=method, url=url, headers=headers)
    accounts_response = session_object.send(accounts_request.prepare())
    print(pretty_request_response(accounts_response))

#--------------------------------------------------------------------------------------------------------

#Certain POST requests will request json body, set to bbody in this script
if len(bbody) > 0:
    accounts_request = requests.Request(method=method, url=url, headers=headers, json=bbody)
    accounts_response = session_object.send(accounts_request.prepare())
    print(pretty_request_response(accounts_response))
