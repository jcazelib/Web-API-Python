"""
Python script used for testing the available CP API endpoints - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#endpoints       |   For Websocket samples, please refer to - https://github.com/awiseib/Python-CPAPI-Library/tree/main/Websockets

This script assumes you've logged into the Client Portal API gateway (either the IBKR Live/Paper account at localhost:5000) and received "Client Login Succeeds"
    Initial set-up instructions - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#get-started

This script breaks-down the CP API endpoints into the following sections:
    SESSION | ACCOUNT  | CONTRACT | OPTION/FUTURES CHAIN | FINANCIAL ADVISOR OPERATIONS
    MARKET DATA | ORDERS | ORDER MONITORING | PORTFOLIO | PORTFOLIO ANALYST | SCANNERS | SUPPRESS | ALERTS 
"""

import json
import requests

#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-INPUTS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-==---=
#==================================================================================================================
baseURL = "localhost:5000"
accountId = "YOUR ACCOUNTID"


#==================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-SESSION-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-===-=-==---=
#==================================================================================================================
##### Comment or uncomment the method & url which you'd like to test below #####

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
#             "orderType": "STP",
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
# replyId = '268bd34a-2826-44dd-aa1d-502831187b31'
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

# method = 'DELETE'
# url = "".join([f'https://{baseURL}/v1/api/iserver/account/{accountId}/order/-1'])


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
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-CP Gateway=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-===--=-=
#====================================================================================================================
headers = {"User-Agent": "python/3.11"}

##### OPTIONAL - for added cleanliness:
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-CP Gateway sending the http request=-===-=-==-=-=-=-----=-=-=-=-==-=-=-=
#====================================================================================================================
##### IF no JSON body & no replybody (i.e. for GET requests) ##### 
if len(body) == 0 and len(replybody) == 0:
    print("-----------REQUEST-----------")
    print(method, url)
    if method == 'GET':
        http_req = requests.get(url=url, verify=False)
    elif method == 'POST' or method == 'DELETE' or method == 'PUT':
        http_req = requests.post(url=url, verify=False)
    print("")
    
    print("-----------RESPONSE-----------")
    req_json = json.dumps(http_req.json(), indent=2)
    print(http_req)
    print(req_json)
        
    

##### Certain POST requests will require a json body, set to body in this script ##### 
if len(body) > 0:
    print("-----------REQUEST-----------")
    print(method, url)
    if method == 'GET':
        http_req = requests.get(url=url, verify=False)
    elif method == 'POST' or method == 'DELETE' or method == 'PUT':
        http_req = requests.post(url=url, verify=False, json=body)
    print("")
    
    print("-----------RESPONSE-----------")
    req_json = json.dumps(http_req.json(), indent=2)
    print(http_req)
    print(req_json)
    

##### Used to send the  POST /iserver/reply/{{replyId}} endpoint - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#place-order-reply #####
if len(replybody) > 0:
    print("-----------REQUEST-----------")
    print(method, url)
    if method == 'GET':
        http_req = requests.get(url=url, verify=False)
    elif method == 'POST':
        http_req = requests.post(url=url, verify=False, json=replybody)
    print("")
    
    print("-----------RESPONSE-----------")
    req_json = json.dumps(http_req.json(), indent=2)
    print(http_req)
    print(req_json)

