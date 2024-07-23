"""
Python script used for testing the available CP API endpoints - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#endpoints     |    For Websocket samples, please refer to - https://github.com/awiseib/Python-CPAPI-Library/tree/main/Websockets | https://github.com/awiseib/Python-CPAPI-Library/tree/main/OAuth/First%20Party   

This script assumes you've already received a Live Session Token & Access Token
    Lines 24 - 27: Enter your consumer_key | access_token | live_session_token | (optional) accountId which is the U-account or DU-account number

This script breaks-down the CP API endpoints into the following sections:
    SESSION | ACCOUNT  | CONTRACT | OPTION/FUTURES CHAIN | FINANCIAL ADVISOR OPERATIONS
    MARKET DATA | ORDERS | ORDER MONITORING | PORTFOLIO | PORTFOLIO ANALYST | SCANNERS | SUPPRESS | ALERTS 
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
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-INPUTS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-==---=
#==================================================================================================================
consumer_key = "YOURCONSUMER"
access_token = "ACCESSTOKEN"
live_session_token = "LIVESESSIONTOKEN"
accountId = "ACCOUNTID"
baseURL = "api.ibkr.com"


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-SESSION-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-==---=
#==================================================================================================================
##### Comment or uncomment the endpoint which you'd like to test below #####


method = 'GET'
url = f'https://{baseURL}/v1/api/portfolio/accounts'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/accounts'

# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/auth/ssodh/init?publish=true&compete=true'      #Initiate brokerage session - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#ssodh-init | https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#auth-sessions-background

# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/auth/status'

# method = 'POST'
# url = f'https://{baseURL}/v1/api/logout'                                       #Logout to end the session

# method = 'GET'
# url = f'https://{baseURL}/v1/api/tickle'

body = []
replybody = []

# method = 'POST'                                                                #Another way to call ssodh/init
# url = f'https://{baseURL}/v1/api/iserver/auth/ssodh/init'
# body = {
#   "publish": True,
#   "compete": True
# }


# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account'                              #Switch accounts - used by Financial Advisors & Introducing Brokers
# body = """
# {
#   "acctId": accountId,
# }


##### NOTE:
##### CONID 265598 corresponds to AAPL stock  |  CONID 12087792 corresponds to EUR.USD FX pair


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-ACCOUNT-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=--=-==
#==================================================================================================================
# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/accounts'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/subaccounts'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/subaccounts2'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/pnl/partitioned'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/acesws/{accountId}/signatures-and-owners'


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-CONTRACT-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-=-=-=
#==================================================================================================================
# method = 'GET'
# url = f'https://{baseURL}/v1/api/trsrv/all-conids/?exchange=NYSE'              #For STOCKS - get all CONIDs by exchange

# method = 'GET'
# url = f'https://{baseURL}/v1/api/trsrv/secdef?conids=265598'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/contract/265598/info'               

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/currency/pairs?currency=USD'          #For FX - get all CONIDs

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/exchangerate?source=JPY&target=USD'   #For FX - get exchange rate

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/contract/265598/info-and-rules?isBuy=true'  

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/contract/265598/algos?addDescription=1&addParams=1'  

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/bond-filters?symbol=BOND&issuerId=e1400715' 

# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/secdef/search'                   
# body = {
#   "symbol": "IBM",
#   "name": True,
#   "secType": "STK"
# }


# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/contract/rules' 
# body = """
# {
#   "conid": "265598",
#   "isBuy": true
# }


# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/strikes?conid=265598&sectype=OPT&month=DEC25'                

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/info?conid=265598&sectype=OPT&month=DEC25&strike=0&right=C'   
 
# method = 'GET'
# url = f'https://{baseURL}/v1/api/trsrv/futures?symbols=ES'                     #for FUTURES - get CONIDs

# method = 'GET'
# url = f'https://{baseURL}/v1/api/trsrv/stocks?symbols=AAPL,IBKR,IBM'           #for STOCKS - get CONIDs

#method = 'GET'
#url = f'https://{baseURL}/v1/api/trsrv/secdef/schedule?assetClass=STK&symbol=AAPL&exchange=NASDAQ&exchangeFilter=NASDAQ' 


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-OPTION/FUTURES CHAIN-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=
#==================================================================================================================
### Step 1 - POST /iserver/secdef/search          
### Step 2 - GET  /iserver/secdef/strikes  
### Step 3 - GET  /iserver/secdef/info     


##### OPTION CHAIN #####
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/secdef/search'                   
# body = {
#   "symbol": "AAPL",
#   "name": True,
#   "secType": "OPT"
# }


# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/strikes?conid=265598&sectype=OPT&month=DEC25'                

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/info?conid=265598&sectype=OPT&month=DEC25&strike=0&right=C'   



##### FUTURE OPTION CHAIN #####       |   #specify the Index's CONID (11004968 for ES index) for steps 2 and 3!!!!
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/secdef/search'                   
# body = {
#   "symbol": "ES",
#   "name": True,
#   "secType": "FUT"
# }

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/strikes?exchange=CME&conid=11004968&sectype=FOP&month=DEC25'       

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/secdef/info?exchange=CME&conid=11004968&sectype=FOP&month=DEC25&strike=0&right=C'


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=--FINANCIAL ADVISOR OPERATIONS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-===
#==================================================================================================================
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account'                              #Switch accounts - used by Financial Advisors & Introducing Brokers
# body = {
#   "acctId":accountId
# }


# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/accounts'          #Get Allocatable Sub-accounts

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/group'             #Get Allocation Groups


# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/group/single'      #Get the details of a specified allocation group
# body = {
#   "name":"Group1"
# }


##### CREATE AN ALLOCATION GROUP #####
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/group'             #Available Equity=A / Equal=E  / Net Liquidation Value=N / CashQuantity=C / Percentages=P / Ratios=R / Shares=S
# body = {
#     "name": "CashEq2",
#     "accounts": [
#         {
#             "name": "DUXXXX123"
#         },
#         {
#             "name": "DUXXXX124"
#         }
#     ],
#     "default_method": "E"
# }


##### CREATE AN ALLOCATION PROFILE #####
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/group'             #Available Equity=A / Equal=E  / Net Liquidation Value=N / CashQuantity=C / Percentages=P / Ratios=R / Shares=S
# body = {
#     "name": "CASH2z",
#     "accounts": [
#         {
#             "amount": 2,
#             "name": "DUXXXX123"
#         },
#         {
#             "amount": 1,
#             "name": "DUXXXX124"
#         }
#     ],
#     "default_method": "C"
# }


##### MODIFY an existing allocation group via - PUT  iserver/account/allocation/group #####


##### DELETE an allocation group
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/group/delete' 
# body = {
# "name": "Group1"
# }


# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/allocation/presets'


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-MARKET DATA-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-==-=-=-===
#==================================================================================================================
###### MARKET DATA SNAPSHOT  |  Needs to be called twice!! #####
# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/marketdata/snapshot?conids=12087792@IDEALPRO&since=0&fields=31,55,6509,84' 



###### HiSTORICAL MARKET DATA #####
# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/marketdata/history?conid=12087792&exchange=IDEALPRO&period=1d&bar=1min&outsideRth=false'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/marketdata/history?conid=12087792&exchange=IDEALPRO&period=10d&bar=1d&outsideRth=false'


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-ORDERS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-====
#==================================================================================================================
##### PLACE ORDER #####
# method = 'POST'
# url = "".join([f'https://{baseURL}/v1/api/iserver/account/{accountId}/orders'])     #Place Orders endpoint - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#place-order

# conid = 265598    
# orders = [
#         {
#             "conid": conid,
#             "orderType": "LMT",
#             "outsideRTH": False,
#             "price": 1,
#             "side": "BUY",
#             "tif": "GTC",
#             "quantity": 1
#         }
# ]

# body = {
#   "orders": orders
# }



##### REPLY TO ORDERS #####
# replyId = '5f8de0bb-a743-4b9e-8439-82686c1a8567'
# method = 'POST'
# url = "".join([f'https://{baseURL}/v1/api/iserver/reply/', replyId])

# replybody = {
#   "confirmed": True
# }



##### WHAT-IF ORDER #####
# method = 'POST'
# url = "".join([f'https://{baseURL}/v1/api/iserver/account/{accountId}/orders/whatif'])

# conid = 265598    
# orders = [
#         {
#             "conid": conid,
#             "orderType": "LMT",
#             "outsideRTH": False,
#             "price": 100,
#             "side": "BUY",
#             "tif": "GTC",
#             "quantity": 1
#         }
# ]

# body = {
#   "orders": orders
# }



##### MODIFY ORDER #####
# method = 'POST'
# url = "".join([f'https://{baseURL}/v1/api/iserver/account/{accountId}/order/{orderId}']) 
# orders = [
#         {
#             "conid": conid,
#             "orderType": "LMT",
#             "outsideRTH": False,
#             "price": 1,
#             "side": "BUY",
#             "tif": "GTC",
#             "quantity": 2
#         }
# ]

# body = {
#   "orders": orders
# }



##### CANCEL A PARTICULAR ORDER #####
# method = 'DELETE'
# url = "".join([f'https://{baseURL}/v1/api/iserver/account/{accountId}/order/{orderId}']) 


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-ORDER MONITORING-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===
#==================================================================================================================
# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/orders'                       #Live Orders


# method = 'GET'
# orderId = '2000983381'
# url = f'https://{baseURL}/v1/api/iserver/account/order/status/{orderId}'       #Order Status


# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/trades'                       #Executions


###### Websockets (sor+{}) - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#ws-order-updates-sub
###### Websocket playground - https://interactivebrokers.github.io/cpwebapi/websockets#websocket-playground
###### URL = wss://api.ibkr.com/v1/api/ws?oauth_token={access_token}
###### Message: {"session":"{sessionId from /tickle}"}


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-PORTFOLIO-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-=-=-=-====
#==================================================================================================================
# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/accounts'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/positions/0'            #Get Open Positions

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/position/265598'        #Get Open Positions (by CONID)

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/allocation'             #Information about the account’s portfolio allocation by Asset Class, Industry and Category

# method = 'POST'
# url = f'https://{baseURL}/v1/api/portfolio/allocation'                         #Information about the account’s portfolio allocation by Asset Class, Industry and Category
# body = {
#   "acctIds": [
#     accountId
#   ]
# }  


# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/positions/invalidate' 

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/meta'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/summary'                #Cash balances & margin details for the given account

# method = 'GET'
# url = f'https://{baseURL}/v1/api/portfolio/{accountId}/ledger'                 #Cash balances & margin details for the given account (broken down by currency)

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/summary/balances'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/summary/margins'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/summary/market_value'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/summary/available_funds'


#===================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-PORTFOLIO ANALYST-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===
#===================================================================================================================
# method = 'POST'
# url = f'https://{baseURL}/v1/api/pa/performance'
# body = {
#   "acctIds": [
#     accountId
#   ],
#   "freq": "D"
# }


# method = 'POST'
# url = f'https://{baseURL}/v1/api/pa/transactions'
# body = {
#   "acctIds": [
#     accountId
#   ],
#   "conids": [
#     265598
#   ],
#   "currency": "USD",
#   "days": 7
# }


#===================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-SCANNER-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-==-=-=-====-===
#===================================================================================================================
# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/scanner/params'

# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/scanner/run'
# body = {
#         "instrument": "STK",
#         "location": "STK.US",
#         "type": "TOP_OPEN_PERC_GAIN",
#         "filter": [
#             {
#                 "code":"priceBelow",
#                 "value":20
#             },
#             {
#                 "code":"usdVolumeAbove",
#                 "value":100000
#             }
#         ]
# }


# method = 'POST'
# url = f'https://{baseURL}/v1/api/hmds/scanner'
# body = {
#         "instrument": "STK",
#         "locations": "STK.US",
#         "scanCode": "TOP_OPEN_PERC_GAIN",
#         "secType": "STK",
#         "filter": [
#             {
#                 "code":"priceBelow",
#                 "value":20
#             },
#             {
#                 "code":"usdVolumeAbove",
#                 "value":100000
#             }
#         ]
# }


#===================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-SUPPRESS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-===
#===================================================================================================================
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/questions/suppress'
# body = {
#   "messageIds":["o451","o163"]
# }


# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/questions/suppress/reset'


#===================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-ALERTS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-===-=
#===================================================================================================================
# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/alerts'

# method = 'GET'
# alertId = '1132135167'
# url = f'https://{baseURL}/v1/api/iserver/account/alert/{alertId}?type=Q'

# method = 'GET'
# url = f'https://{baseURL}/v1/api/iserver/account/mta'  


##### CREATE ALERT #####   
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/alert'
# body = see: https://github.com/awiseib/Python-CPAPI-Library/tree/main/Alerts


##### ACTIVATE ALERT #####
# method = 'POST'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/alert/activate'
# body = {
#     "alertId":2051736314,
#     "alertActive": 0
# }        


##### DELETE ALERT #####
# method = 'DELETE'
# alertId = '1132135167'
# url = f'https://{baseURL}/v1/api/iserver/account/{accountId}/alert/{alertId}'        


#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-OAuth 1.0a=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-===--=-=
#====================================================================================================================
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
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-OAuth 1.0a sending the http request=-===-=-==-=-=-=-----=-=-=-=-==-=-=-=
#====================================================================================================================
##### IF no JSON body & no replybody (i.e. for GET requests) #####
if len(body) == 0 and len(replybody) == 0:
    accounts_request = requests.Request(method=method, url=url, headers=headers)
    accounts_response = session_object.send(accounts_request.prepare())
    print(pretty_request_response(accounts_response))


##### Certain POST requests will request json body, set to 'body' in this script #####
if len(body) > 0:
    accounts_request = requests.Request(method=method, url=url, headers=headers, json=body)
    accounts_response = session_object.send(accounts_request.prepare())
    print(pretty_request_response(accounts_response))
    

##### To send the POST /iserver/reply/{{replyId}} endpoint - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#place-order-reply #####
if len(replybody) > 0:
    print("sending Reply Order Endpoint:")
    accounts_request = requests.Request(method=method, url=url, headers=headers, json=replybody)
    accounts_response = session_object.send(accounts_request.prepare())
    print(pretty_request_response(accounts_response))   

