"""
IBKR Model Portfolios (Web API) tester 2026 
- Replace BearerToken below with the token returned from POST /gw/api/v1/sso-sessions
- Replace SessionToken below with the "session" value returned from /tickle
- Ensure the GET /iserver/account/allocation/models endpoint is called 1st, prior to other /fa/model endpoints

Documentation: 
https://api.ibkr.com/gw/swagger-ui.html#/Trading%20FA%20Model%20Portfolios


POST /fa/model/tws-invest-divest supports:
1. A single U-account ID            -> "account": "DUXXXX123"
2. A list of U-account IDs          -> "accountList": ["DUXXXX123","DUXXXX124", "DUXXXX125"]
3. An FA pre-trade allocation group -> "group": "Group1"  or  "group": "All" (if used, the investment amount is divided equally between the group's accounts)

/tws-invest-divest can accept a named group (or "All"). If used, the investment amount is divided equally between the group's accounts. A list of accounts can also be provided. 

Pros & cons of using /tws-invest-divest vs. /invest-divest:
With tws-invest-divest, the user can have instruments in multiple currencies in the model — with invest-divest, only a single currency is possible.
tws-invest-divest allows multiple models to be invested in with one request, whereas invest-divest supports only a single model per request. However, invest-divest allows a different investment amount to be specified per account (since groups are not supported and each account's amount is set individually), while tws-invest-divest splits one amount equally across all accounts when a group or account list is used.
"""

import json
import pprint
import time
import requests

#====================================================================================================================
#-------------------------------------------INPUTS-------------------------------------------------------------------
#====================================================================================================================
BearerToken  = "XXXXX"
SessionToken = "XXXXX"
modelCode    = "MODEL-API-DEMO"
accountId    = "DUXXXX123"
cpapi_url    = "https://api.ibkr.com/v1/api"

#====================================================================================================================
#-----------------------------------------1. PRE REQS----------------------------------------------------------------
#====================================================================================================================
# method = "POST"
# url = f"{cpapi_url}/iserver/auth/ssodh/init"
# json_content = {"publish":True, "compete":True}

method = "GET"
# url = f"{cpapi_url}/iserver/accounts"
url = f"{cpapi_url}/iserver/account/allocation/models"              #CALL THIS PRIOR TO USING ANY MODEL ENDPOINTS BELOW!!!

# method = "POST"
# url = f"{cpapi_url}/iserver/questions/suppress"
# json_content = {
#   "messageIds": ["o163", "o354", "o382", "o383", "o451", "o10164", "o10223", "p6", "o10153", "o10331"]
# }

# method = "POST"
# url = f"{cpapi_url}/fa/fa-preset/get"
# json_content = {
#   "reqID": 127,
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/fa-preset/save"
# json_content = {
#   "avoidNegativeCashInIndependent": False,
#   "closeDivestIndependentPosition": False,
#   "fullyInvestExistingLongPositions": False,
#   "keepModelOpen": False,
#   "preferCrossWithIndependent": False,
#   "preferTransferFromIndependent": False,
#   "reqID": 128,
#   "roundAllocationQuantityToExchangeBoardLot": False,
#   #"subscriptionStatus": 1,        #do not pass subscriptionStatus with this request
#   "useNonBaseCcy": False,
#   "useToleranceRange": False
# }

#====================================================================================================================
#----------------------------------------2. MODEL PORTFOLIO ENDPOINTS (Phase 1)--------------------------------------
#====================================================================================================================
##### Portfolio requests using mp.{modelCode} #####
# method = "GET"
# url = f"{cpapi_url}/portfolio/subaccounts"
# url = f"{cpapi_url}/portfolio/{accountId}/summary"
# url = f"{cpapi_url}/portfolio/{accountId}/ledger"
# url = f"{cpapi_url}/portfolio2/{accountId}/positions"
# url = f"{cpapi_url}/portfolio/{accountId}/summary?model=MP.{modelCode}"
# url = f"{cpapi_url}/portfolio/{accountId}/ledger?model=MP.{modelCode}"
# url = f"{cpapi_url}/portfolio2/{accountId}/positions?model=MP.{modelCode}"

##### New Models Endpoints 2026 #####
# method = "POST"
# url = f"{cpapi_url}/fa/model/list"
# json_content = {
#   "reqID": 123,
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/save"
# json_content = {
#   "reqID": 126,
#   "model": f"{modelCode}",
#   "desc": "DEMO-MODEL-LONGONLY",
#   "isStatic": False,
#   "positionTargets": [
#       {"cid": 270639, "trgt": 0.45},
#       {"cid": 8314,   "trgt": 0.45}
#   ],
#   "cashTargets": [
#       {"ccy": "USD", "trgt": 0.1}
#   ],
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/invest-divest"     #invest single account into model $1000
# json_content = {
#   "reqID": 1302,
#   "model": f"{modelCode}",
#   "accountList": [
#       {"account": "DUXXXX123", "amtToInvest": 1000}
#   ],
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/invest-divest"     #invest multiple accounts into model $3000
# json_content = {
#   "reqID": 1302,
#   "model": f"{modelCode}",
#   "accountList": [
#       {"account": "DUXXXX123", "amtToInvest": 1000},
#       {"account": "DUXXXX124", "amtToInvest": 1000},
#       {"account": "DUXXXX125", "amtToInvest": 1000}
#   ],
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/submit-transfers"
# json_content = {
#   "reqID": 132,
#   "fpOrderId": 1,                                #replace with the transfersInstructionId returned from POST /fa/model/invest-divest or POST /fa/model/tws-invest-divest
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/iserver/account/{modelCode}/orders"
## url = f"{cpapi_url}/iserver/account/{modelCode}/orders/whatif"
# json_content = {                                  #Place Order - Invest
#   "orders": [
#     {
#       "quantity": 2,
#       "orderType": "LMT",
#       # "useAdaptive": False,
#       "price": 252,
#       "tif": "GTC",
#       "outsideRTH": True,
#       # "allOrNone": False,
#       # "acctId": "MCPAPI01",
#       "isModel": True,
#       "cOID": 8314,
#       "conidex": 8314,
#       "side": "BUY",
#       "jsonPayload": {
#         "allocation_profile": {
#           "alloc_type": "SHARE",                                 #Use SHARE + quantity for share quantities | CASH + cashQty for cash quantity orders
#           "allocations": [{"account": accountId, "amount": 2}]   #For multiple accounts/amounts, ensure that quantity or cashQty used above = the sum of each "amount" used here
#         }
#       }
#     }
#   ]
# }

# url = f"{cpapi_url}/iserver/account/{modelCode}/orders"
# json_content = {                                  #Place Order - Inline Profiles
#   "orders": [
#     {
#       "cashQty": 3000,
#       "orderType": "MKT",
#       #"price": 1,
#       "tif": "DAY",
#       #"outsideRTH": True,
#       "isModel": True,
#       "conidex": 265598,
#       "side": "BUY",
#       #"useAdaptive": False,      
#       #"allOrNone": False,
#       #"acctId": "MODEL-API-DEMO",
#       #"cOID": 8314,            
#       "jsonPayload": {
#         "allocation_profile": {
#           "alloc_type": "CASH",
#           "allocations": [
#             {
#               "account": "DUXXXX123",
#               "amount": 1000
#             },
#             {            
#               "account": "DUXXXX124",
#               "amount": 1000
#             },
#             {
#               "account": "DUXXXX125",
#               "amount": 1000                                          
#             }
#           ]
#         }
#       }
#     }
#   ]
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/invest-divest-positions"
# json_content = {
#   "reqID": 129,
#   "model": f"{modelCode}",
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/accounts-details"
# json_content = {
#   "calcPnls": True,
#   "model": f"{modelCode}",
#   "reqID": 1232
#   # "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/positions"
# json_content = {
#   "reqID": 125,
#   "model": f"{modelCode}",
#   "sortDirection": "DESC",
#   "sortField": "actl",
#   "limit": 10,
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/fa/model/summary"
# json_content = {
#   "reqID": 124,
#   "model": f"{modelCode}",
#   "subscriptionKey": ""
# }

#====================================================================================================================
#--------------------------------------------3. REBALANCE ENDPOINTS (Phase 2)----------------------------------------
#====================================================================================================================
##### New Rebalance Endpoints 2026 #####
# method = "POST"
# url = f'{cpapi_url}/fa/model/rebalance/to-existing-targets'      #Use "rebalanceType": "MODEL" with rebalance orders
# json_content = {
#   "reqID": 398899,
#   "model": f"{modelCode}",
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/iserver/account/{modelCode}/orders"
# {
#     "orders": [
#         {
#             "cashQty": 6046.13,
#             "orderType": "LMT",
#             "price": 1,
#             "tif": "DAY",
#             "outsideRTH": False,
#             "isModel": True,
#             "conid": "268084",
#             "side": "BUY",
#             "jsonPayload": {
#                 "allocation_profile": {
#                     "alloc_type": "CASH",
#                     "allocations": [
#                         {
#                             "account": "DUXXXX123",
#                             "amount": 6046.13
#                         }
#                     ]
#                 }
#             },
#             "trgtPercent": 60.00,
#             "rebalanceType": "MODEL"
#         }
#     ]
# }


# method = "POST"
# url = f'{cpapi_url}/fa/model/rebalance/to-new-targets'            #Use "rebalanceType": "MODEL" with rebalance orders
# json_content = {
#   "reqID": 398896,
#   "model": f"{modelCode}",
#   "positionTargets": [
#     {"conid": 268084, "target": 0.35, "locked": False},
#     {"conid": 270639, "target": 0.5,  "locked": False}
#   ],
#   "cashTargets": [
#     {"ccy": "USD", "target": 0.15, "locked": False}
#   ],
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/iserver/account/{modelCode}/orders"
# json_content = {
#     "orders": [
#         {
#             "cashQty": 6012.58,
#             "orderType": "LMT",
#             #"useAdaptive": True,
#             "price": 1,
#             "tif": "DAY",
#             "outsideRTH": False,
#             #"allOrNone": False,
#             #"acctId": "TestCPAPI4",
#             "isModel": True,
#             #"cOID": "dvcpapitest2",
#             "conidex": "268084",
#             "side": "BUY",
#             "jsonPayload": {
#                 "allocation_profile": {
#                     "alloc_type": "CASH",
#                     "allocations": [
#                         {
#                             "account": "DUXXXX123",
#                             "amount": 6012.58
#                         }
#                     ]
#                 }
#             },
#             "trgtPercent": 90,
#             "rebalanceType": "TARGET"
#         }
#     ]
# }


# method = "POST"
# url = f'{cpapi_url}/fa/model/rebalance/to-specific-targets'
# json_content = {
#   "reqID": 398899,
#   "model": f"{modelCode}",
#   "positionTargets": [
#     {"conid": 268084, "target": 0.35, "locked": False}
#   ],
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f"{cpapi_url}/iserver/account/{modelCode}/orders"
# json_content = {
#     "orders": [
#         {
#             "cashQty": 6046.13,
#             "orderType": "LMT",
#             #"useAdaptive": True,
#             "price": 1,
#             "tif": "DAY",
#             "outsideRTH": False,
#             #"allOrNone": False,
#             #"acctId": "TestCPAPI4",
#             "isModel": True,
#             #"cOID": "dvcpapitest1",
#             "conidex": "268084",
#             "side": "BUY",
#             "jsonPayload": {
#                 "allocation_profile": {
#                     "alloc_type": "CASH",
#                     "allocations": [
#                         {
#                             "account": "DUXXXX123",
#                             "amount": 6046.13
#                         }
#                     ]
#                 }
#             },
#             "trgtPercent": 60.00,
#             "rebalanceType": "MODEL"
#         }
#     ]
# }

# method = "POST"
# url = f'{cpapi_url}/fa/model/tws-invest-divest'           #An account / account_list / group can invest in multiple models in the same request. One can specify one of targetAmt/targetPercent/amtToInvest for each model separately
# json_content = {
#   "reqID": 398889,
#   "account": f"{accountId}",
##  "accountList": ["DUXXX123", "DUXXX124", "DUXXX125"],
##  "group": "Group1"  
##  "group": "All"
#   "modelList": [
#     {
#       "investCurrency": "USD",
#       "amtToInvest": 1000,
#       "model": f"{modelCode}"
#     },
#     {
#       "investCurrency": "USD",
#       "amtToInvest": 2000,
#       "model": f"{modelCode}"
#     }
#   ],
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f'{cpapi_url}/fa/is-full-master'   
# json_content = {
#   "reqID": 398899,
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f'{cpapi_url}/fa/model/cash-analyzer' 
# json_content = {
#   "reqID": 398899,
#   "subscriptionKey": ""
# }

# method = "POST"
# url = f'{cpapi_url}/logout'

#====================================================================================================================
#----------------------------------------HTTP REQUEST 1--------------------------------------------------------------
#====================================================================================================================
RESP_HEADERS_TO_PRINT = ["Content-Type", "Content-Length", "Date", "Set-Cookie", "User-Agent"]

def formatted_HTTPrequest(resp: requests.Response) -> str:
    req = resp.request
    rqh = "\n".join(f"{k}: {v}" for k, v in req.headers.items()).replace(", ", ",\n    ")
    rqb = req.body or ""

    try:
        rsb = f"\n{pprint.pformat(resp.json())}\n" if resp.text else ""
    except json.JSONDecodeError:
        rsb = resp.text
    rsh = "\n".join(f"{k}: {v}" for k, v in resp.headers.items() if k in RESP_HEADERS_TO_PRINT)

    time.sleep(1)
    print("")
    return "\n".join([
        "-----------REQUEST-----------",
        f"{req.method} {req.url}",
        "",
        rqh,
        f"{rqb}",
        "",
        "-----------RESPONSE-----------",
        f"{resp.status_code} {resp.reason}",
        rsh,
        f"{rsb}\n",
    ])


#====================================================================================================================
#----------------------------------------HTTP REQUEST 2--------------------------------------------------------------
#====================================================================================================================
CPAPI_headers = {
    "Authorization": f"Bearer {BearerToken}",
    "Cookie":        f"api={SessionToken}",
    "User-Agent":    "model_tester_python/3.11",
}

if method == "GET":
    CPAPI_request = requests.get(url=url, headers=CPAPI_headers)
elif method == "POST":
    CPAPI_request = requests.post(url=url, headers=CPAPI_headers, json=json_content or None)

print(formatted_HTTPrequest(CPAPI_request))
