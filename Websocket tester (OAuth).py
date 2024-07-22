"""
Python script used for testing Websockets via CP API - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#websockets   |   Certain requests like sbd+{} ssd+{} and sld+{} will require the IBKR Account ID {accountId} be included 

This script assumes you've already received a Live Session Token, Access Token, & then Initiated a Brokerage Session  [POST https://api.ibkr.com/v1/api/iserver/auth/ssodh/init?publish=true&compete=true]
    Lines 24 - 27: Enter your consumer_key | access_token | live_session_token | (optional) accountId which is the U-account or DU-account number

The Websocket request to send is specified in line 116:
    ws.send('smd+12087792+{"fields":["84","85","86","88","7219"]}')    
"""

import json
import requests
import random
import base64
import pprint
from datetime import datetime
from urllib.parse import quote, quote_plus
from Crypto.Hash import SHA256, HMAC, SHA1
import time

#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=--==-INPUTS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-==
#====================================================================================================================
consumer_key = "YOURCONSUMER"
access_token = "ACCESSTOKEN"
live_session_token = "LIVESESSIONTOKEN"
accountId = "ACCOUNTID"


#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-OAuth 1.0a=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-===--=-=
#====================================================================================================================
baseURL = "api.ibkr.com"
method = 'GET'
url = f'https://{baseURL}/v1/api/tickle'                                                #First make a request to the /tickle endpoint and save the returned session value.

session_object = requests.Session()
realm = "limited_poa"

RESP_HEADERS_TO_PRINT = ["Content-Type", "Content-Length", "Date", "Set-Cookie", "User-Agent"]

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

# print("CONSUMER KEY = ", consumer_key)
# print("")


#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-WEBSOCKETS=-===-=-==-=-=-=-----=-=-=-=-==-=-=-=-=-=-=-==-===-=-==-=---==
#====================================================================================================================
import websocket

tickle_request = requests.request(method=method, url=url, headers=headers)
print(pretty_request_response(tickle_request))

global TICKLE_COOKIE
TICKLE_COOKIE = tickle_request.json()['session']

def on_open(ws):
    print("Opened Connection")
    print("-----------------")
    time.sleep(1)
    
    ##### Send the ws request (Market data / Order Updates / PnL / etc.) #####                 #Specify the Websocket request - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#websockets
    ws.send('smd+12087792+{"fields":["84","85","86","88","7219"]}')                            #Available Market Data fields  - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#market-data-fields   
    #ws.send(f'sbd+{accountId}+12087792+IDEALPRO')          
    #ws.send('smh+265598+{"period": "1d","bar": "1min","source": "trades","format": "%o/%c/%h/%l"}')           
      
    #ws.send(f'ssd+{accountId}+{"keys":["AccruedCash-S","ExcessLiquidity-S"],"fields":["currency","monetaryValue"]}')
    #ws.send(f'sld+{accountId}+{"keys":["LedgerListBASE","LedgerListEUR"], "fields":["cashBalance","exchangeRate"]}')

    #ws.send('sor+{}')
    #ws.send('str+{"realtimeUpdatesOnly": true, "days": 7}')
    #ws.send('spl+{}')
    #ws.send('tic')  
    
    
    ##### Pass-in a list of CONIDs to stream market data for (CONID_list) #####
    # for item in CONID_list:
    #     string1 = 'smd+'                                                                
    #     string2 = f'{item}'
    #     string3 = '+{"fields":["84","85","86","88","7219"]}'
    #     smdreq = string1+string2+string3
    #     print("smd request = ", smdreq)                                                         #Print the CONID+smd request we're making via Websocket
    
    #     ws.send(smdreq)                                         
    #     time.sleep(0.5)
    
    ##### NOTE: "Invalid format specifier" error - adjust the ws.send() request and ensure this is a string which contains the type of request/accountId/CONID/etc. #####


def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, r1, r2):
    print("## CLOSED! ##")
    print(f"r1:{r1}")
    print(f"r2:{r2}")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        url=f"wss://{baseURL}/v1/api/ws?oauth_token={access_token}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=["User-Agent: python/3.11"],
        cookie=f"api={TICKLE_COOKIE}"
    )
    ws.run_forever()
    
    
