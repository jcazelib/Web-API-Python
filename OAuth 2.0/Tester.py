"""
Python script when demonstrates the various Trading Web API endpoints. 

This script assumes you've already received an SSO BearerToken & SessionToken (enter both under the INPUTS section)

Requests are broken-down into the following sections:
    SESSION | ACCOUNT  | ALERTS | CONTRACT | OPTION/FUTURES CHAIN | FINANCIAL ADVISOR OPERATIONS
    MARKET DATA | ORDERS | ORDER MONITORING | PORTFOLIO | PORTFOLIO ANALYST | SCANNERS | SUPPRESS | ALERTS | FORECASTEX
"""

import json
import time
import pprint
import requests
  
#====================================================================================================================
#-------------------------------------------INPUTS-------------------------------------------------------------------
#====================================================================================================================
BearerToken = "XXXXX"
SessionToken = "XXXXX"
accountId = "DUXXXX123"

#====================================================================================================================
#-------------------------------------------BASE URLs----------------------------------------------------------------
#====================================================================================================================
host = 'api.ibkr.com'
oauth2Url = 'https://api.ibkr.com/oauth2'
gatewayUrl = 'https://api.ibkr.com/gw'
clientPortalUrl = 'https://api.ibkr.com'
audience = '/token'  

#====================================================================================================================
#--------------------------------------------SESSION-----------------------------------------------------------------
#====================================================================================================================
def session_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/tickle'   
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  
    
    url_2 = f'{clientPortalUrl}/v1/api/sso/validate'            
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))  
                 
    url_3 = f'{clientPortalUrl}/v1/api/iserver/auth/ssodh/init'   
    body_3 = {
      "publish": True,
      "compete": True
    }
    
    request_3 = requests.post(url=url_3, headers=CPAPI_headers, json=body_3)                      
    print(formatted_HTTPrequest(request_3))  
    time.sleep(.5)
                         
    url_4 = f'{clientPortalUrl}/v1/api/iserver/accounts'     
    request_4 = requests.get(url=url_4, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_4))  
                        
    url_5 = f'{clientPortalUrl}/v1/api/iserver/auth/status'                             
    request_5 = requests.post(url=url_5, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_5))


#====================================================================================================================
#-------------------------------------------ACCOUNT------------------------------------------------------------------
#====================================================================================================================
def account_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/auth/ssodh/init'   
    body_1 = {
      "publish": True,
      "compete": True
    }
    request_1 = requests.post(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1))  
    time.sleep(.2)
    
    url_2 = f'{clientPortalUrl}/v1/api/iserver/accounts'     
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))  
    
    url_3 = f'{clientPortalUrl}/v1/api/acesws/{accountId}/signatures-and-owners'
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))
    
    url_4 = f'{clientPortalUrl}/v1/api/iserver/account/pnl/partitioned'
    request_4 = requests.get(url=url_4, headers=CPAPI_headers)      
    request_4x = requests.get(url=url_4, headers=CPAPI_headers)    
    preflight = formatted_HTTPrequest(request_4)      
    print(formatted_HTTPrequest(request_4x))
    
    url_5 = f'{clientPortalUrl}/v1/api/iserver/account'
    body_5 = {
      "acctId": accountId
    }
    request_5 = requests.post(url=url_5, headers=CPAPI_headers, json=body_5)                   
    print(formatted_HTTPrequest(request_5))
    
    
#====================================================================================================================
#-------------------------------------------ALERTS-------------------------------------------------------------------
#====================================================================================================================
def alerts_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/alert' 
    body_1 = {
        "alertMessage": "AAPL Test!!", 
        "alertName": "AAPL Price Alert",       
        "alertRepeatable": 0,        
        "expireTime":"20240830-12:00:00",
        "conditions": [ 
            {
            "conidex": "265598@SMART",      # CONID@exchange
            "logicBind": "n",               # If you have one condition, use "n". If you want to use "AND" logic, use "a". If you want to use "OR" logic, use "o"
            "operator": ">=", 
            "triggerMethod": "0", 
            "type": 1,                      # Types: 1-Price, 3-Time, 4-Margin, 5-Trade, 6-Volume, 7: MTA market 8: MTA Position, 9: MTA Acc. Daily PN&
            "value": "220"                  # For Price, use your price, for time, set a time, etc.
            }
        ],
        # "email": "emailname@domain.com",  # Your email here.
        "iTWSOrdersOnly": 0,                # You can specify if you only want this to trigger for TWS, "1", or for all platforms (such as the API), "0"
        "outsideRth": 0,
        "sendMessage": 0,      
        "showPopup": 0,                     # This is specific for TWS alert pop-ups. Generally unnecessary for CPAPI use.
        "tif": "GTC"   
    }   
    request_1 = requests.post(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1)) 
    
    url_2 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/alerts' 
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2)) 
    
    alertId ="568160007"
    url_3 = f'{clientPortalUrl}/v1/api/iserver/account/alert/{alertId}?type=Q' 
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3)) 
    
    url_4 = f'{clientPortalUrl}/v1/api/iserver/account/mta' 
    request_4 = requests.get(url=url_4, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_4))     
    
    url_5 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/alert/activate' 
    body_5 = {
        "alertId": 123456789,
        "alertActive": 0
    }                    
    request_5 = requests.post(url=url_5, headers=CPAPI_headers, json=body_5)   
    print(formatted_HTTPrequest(request_5))     
    
    alertId ="568160007"
    url_6 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/alert/{alertId}' 
    request_6 = requests.delete(url=url_6, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_6))        


#====================================================================================================================
#-------------------------------------------CONTRACT-----------------------------------------------------------------
#====================================================================================================================
def contract_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/trsrv/secdef?conids=265598'
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  

    url_2 = f'{clientPortalUrl}/v1/api/trsrv/all-conids/?exchange=NYSE' 
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))   
    
    url_3 = f'{clientPortalUrl}/v1/api/iserver/contract/265598/info'      
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))   
             
    url_4 = f'{clientPortalUrl}/v1/api/iserver/currency/pairs?currency=USD'         
    request_4 = requests.get(url=url_4, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_4))   
             
    url_5 = f'{clientPortalUrl}/v1/api/iserver/exchangerate?source=JPY&target=USD'   
    request_5 = requests.get(url=url_5, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_5))  
    
    url_6 = f'{clientPortalUrl}/v1/api/iserver/contract/265598/info-and-rules?isBuy=true'  
    request_6 = requests.get(url=url_6, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_6))  
    
    url_7 = f'{clientPortalUrl}/v1/api/iserver/contract/265598/algos?addDescription=1&addParams=1'  
    request_7 = requests.get(url=url_7, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_7))  
    
    url_8 = f'{clientPortalUrl}/v1/api/iserver/secdef/bond-filters?symbol=BOND&issuerId=e1400715' 
    request_8 = requests.get(url=url_8, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_8))
    
    url_9 = f'{clientPortalUrl}/v1/api/iserver/secdef/search'                   
    body_9 = {
      "symbol": "IBM",
      "name": True,
      "secType": "STK"
    }
    request_9 = requests.post(url=url_9, headers=CPAPI_headers, json=body_9)                      
    print(formatted_HTTPrequest(request_9))
    
    url_10 = f'{clientPortalUrl}/v1/api/iserver/contract/rules' 
    body_10 = {
      "conid": "265598",
      "isBuy": True
    }
    request_10 = requests.post(url=url_10, headers=CPAPI_headers, json=body_10)                      
    print(formatted_HTTPrequest(request_10))
    
    url_11 = f'{clientPortalUrl}/v1/api/trsrv/futures?symbols=ES'                    
    request_11 = requests.get(url=url_11, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_11))
    
    url_12 = f'{clientPortalUrl}/v1/api/trsrv/stocks?symbols=AAPL,IBKR,IBM'           
    request_12 = requests.get(url=url_12, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_12))
    
    url_13 = f'{clientPortalUrl}/v1/api/trsrv/secdef/schedule?assetClass=STK&symbol=AAPL&exchange=NASDAQ&exchangeFilter=NASDAQ' 
    request_13 = requests.get(url=url_13, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_13))
    
    url_14 = f'{clientPortalUrl}/v1/api/contract/trading-schedule?conid=8314&exchange=SMART'
    request_14 = requests.get(url=url_14, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_14))   
       
#====================================================================================================================
#-------------------------------------------FINANCIAL ADVISOR OPERATIONS-------------------------------------------------------------------
#====================================================================================================================
###### Available Equity=A    /  Equal=E   /  Net Liquidation Value=N   /   CashQuantity=C   /     Percentages=P    /    Ratios=R    / Shares=S #####

def financialadvisor_endpoints(bearer_token, CPAPI_headers):    
    url_1 = f'{clientPortalUrl}/v1/api/iserver/account'
    body_1 = {
      "acctId": "All"
    }
    request_1 = requests.get(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1))
    
    url_2 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/accounts'          #Get Allocatable Sub-accounts
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))
    
    url_3 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/group'             #Get Allocation Groups
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))
    
    url_4 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/group/single'      #Get the details of a specified allocation group
    body_4 = {
      "name":"Group1"
    }
    request_4 = requests.post(url=url_4, headers=CPAPI_headers, json=body_4)                      
    print(formatted_HTTPrequest(request_4))
    
    
    #### CREATE AN ALLOCATION GROUP #####
    url_5 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/group'             #Available Equity=A / Equal=E  / Net Liquidation Value=N / CashQuantity=C / Percentages=P / Ratios=R / Shares=S
    body_5 = {
        "name": "Group1",
        "accounts": [
            {
                "name": "DUXXXX123"
            },
            {
                "name": "DUXXXX124"
            }
        ],
        "default_method": "E"
    }
    request_5 = requests.post(url=url_5, headers=CPAPI_headers, json=body_5)                      
    print(formatted_HTTPrequest(request_5))
    
    
    #### CREATE AN ALLOCATION PROFILE #####
    url_6 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/group'             #Available Equity=A / Equal=E  / Net Liquidation Value=N / CashQuantity=C / Percentages=P / Ratios=R / Shares=S
    body_6 = {
        "name": "Profile1",
        "accounts": [
            {
                "amount": 2,
                "name": "DUXXXX123"
            },
            {
                "amount": 1,
                "name": "DUXXXX124"
            }
        ],
        "default_method": "C"
    }
    request_6 = requests.post(url=url_6, headers=CPAPI_headers, json=body_5)                      
    print(formatted_HTTPrequest(request_6))
    
    
    #### MODIFY an ALLOCATION GROUP #####
    url_7 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/group'      
    body_7 = {
        "name": "Group1",
        "accounts": [
            {
                "name": "DUXXXX123"
            },
            {
                "name": "DUXXXX124"
            }
        ],
        "default_method": "N"
    }
    request_7 = requests.put(url=url_7, headers=CPAPI_headers, json=body_7)                      
    print(formatted_HTTPrequest(request_7))
    
    
    #### DELETE an ALLOCATION GROUP #####
    url_8 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/group/delete' 
    body_8 = {
    "name": "Group1"
    }
    request_8 = requests.post(url=url_8, headers=CPAPI_headers, json=body_8)                      
    print(formatted_HTTPrequest(request_8))
    
    
    url_9 = f'{clientPortalUrl}/v1/api/iserver/account/allocation/presets'
    request_9 = requests.get(url=url_9, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_9))


#====================================================================================================================
#-------------------------------------------MARKET DATA--------------------------------------------------------------
#====================================================================================================================
def marketdata_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/accounts'     
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  
    
    url_2 = f'{clientPortalUrl}/v1/api/iserver/marketdata/snapshot?conids=265598@SMART&fields=31,55,6509,84'
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)    
    print(formatted_HTTPrequest(request_2))     

    url_2duplicate = url_2
    request_2duplicate = requests.get(url=url_2duplicate, headers=CPAPI_headers)    
    print(formatted_HTTPrequest(request_2duplicate))                                     
    
    url_3 = f'{clientPortalUrl}/v1/api/iserver/marketdata/history?conid=265598&exchange=SMART&period=5d&bar=1d&outsideRth=false'     
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3)) 
    
    
#====================================================================================================================
#-------------------------------------------OPTIONS/FUTURES CHAINS---------------------------------------------------
#====================================================================================================================  
def optionchain_endpoints(bearer_token, CPAPI_headers):  
    url_1 = f'{clientPortalUrl}/v1/api/iserver/secdef/search?symbol=AAPL'  
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  
    
    url_2 = f'{clientPortalUrl}/v1/api/iserver/secdef/strikes?conid=265598&sectype=OPT&month=DEC25'
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))  
    
    url_3 = f'{clientPortalUrl}/v1/api/iserver/secdef/info?conid=265598&sectype=OPT&month=DEC25&strike=0'
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))  

def futuresoptionchain_endpoints(bearer_token, CPAPI_headers):  
    url_4 = f'{clientPortalUrl}/v1/api/iserver/secdef/search'  
    body_4 = {
      "symbol": "ES",
      "name": True,
      "secType": "FOP"
    }
    request_4 = requests.post(url=url_4, headers=CPAPI_headers, json=body_4)                      
    print(formatted_HTTPrequest(request_4))  
    
    url_5 = f'{clientPortalUrl}/v1/api/iserver/secdef/strikes?conid=11004968&sectype=FOP&month=DEC25&exchange=CME'
    request_5 = requests.get(url=url_5, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_5))  
    
    url_6 = f'{clientPortalUrl}/v1/api/iserver/secdef/info?conid=11004968&sectype=FOP&month=DEC25&strike=0&exchange=CME'
    request_6 = requests.get(url=url_6, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_6))  


#====================================================================================================================
#-------------------------------------------ORDERS-------------------------------------------------------------------
#====================================================================================================================
def orders_endpoints(bearer_token, CPAPI_headers): 
    ##### WHAT-IF ORDER #####
    url_1 = "".join([f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/orders/whatif'])
       
    body_1 = {
      "orders": [
        {
          "side": "BUY",
          "quantity": 1,
          "conid": 265598,               #IBKR Contract Identifier (CONID) for AAPL Stock
          "orderType": "LMT",
          "listingExchange": "SMART",
          "price": 1,
          "tif": "DAY",
          "outsideRTH": False
        }
      ]
    }

    request_1 = requests.post(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1))
    
    ##### REPLY TO ORDERS #####
    replyId = '1f2de3bb-a456-7b8e-0123-45678c1a9012'
    url_2 = "".join([f'{clientPortalUrl}/v1/api/iserver/reply/', replyId])
    replybody = {
      "confirmed": True
    }
    request_2 = requests.post(url=url_2, headers=CPAPI_headers, json=replybody)                      
    print(formatted_HTTPrequest(request_2))
    
    ##### CANCEL A PARTICULAR ORDER #####
    orderId= "12345"                          
    url_3 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/order/{orderId}'
    request_3 = requests.delete(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))
    
    ##### CANCEL ALL OPEN ORDERS #####
    # orderId= "-1"                          
    # url_3 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/order/{orderId}'
    # request_3 = requests.delete(url=url_3, headers=CPAPI_headers)                      
    # print(formatted_HTTPrequest(request_3))
    

#====================================================================================================================
#-------------------------------------------ORDER MONITORING---------------------------------------------------------
#====================================================================================================================
def ordermonitoring_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/account/orders'                   
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)    
    print(formatted_HTTPrequest(request_1))
    
    url_1duplicate=url_1
    request_1duplicate = requests.get(url=url_1duplicate, headers=CPAPI_headers)    
    print(formatted_HTTPrequest(request_1duplicate))
        
    orderId = '0123456789'                                                     #Replace with a valid Order ID
    url_2 = f'{clientPortalUrl}/v1/api/iserver/account/order/status/{orderId}'    
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))  
    
    url_3 = f'{clientPortalUrl}/v1/api/iserver/account/trades'                        
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))  
    
    url_3duplicate = f'{clientPortalUrl}/v1/api/iserver/account/trades'                        
    request_3duplicate = requests.get(url=url_3duplicate, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3duplicate))  
    
    
#====================================================================================================================
#-------------------------------------------PORTFOLIO----------------------------------------------------------------
#====================================================================================================================
def portfolio_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/portfolio/accounts'
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  
    
    url_2 = f'{clientPortalUrl}/v1/api/portfolio/subaccounts'
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))
        
    url_3 = f'{clientPortalUrl}/v1/api/portfolio/{accountId}/positions/0'            
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)     
    print(formatted_HTTPrequest(request_3))  
    
    url_3duplicate = url_3            
    request_3duplicate = requests.get(url=url_3duplicate, headers=CPAPI_headers)     
    print(formatted_HTTPrequest(request_3duplicate))  
    
    url_4 = f'{clientPortalUrl}/v1/api/portfolio/{accountId}/position/265598'        
    request_4 = requests.get(url=url_4, headers=CPAPI_headers)  
    print(formatted_HTTPrequest(request_4))  
    
    url_5 = f'{clientPortalUrl}/v1/api/portfolio/{accountId}/allocation'             
    request_5 = requests.get(url=url_5, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_5))  
    
    url_6 = f'{clientPortalUrl}/v1/api/portfolio/allocation'                         
    body_6 = {
      "acctIds": [
        accountId
      ]
    }  
    request_6 = requests.post(url=url_6, headers=CPAPI_headers, json=body_6)                      
    print(formatted_HTTPrequest(request_6))  
    
    url_7 = f'{clientPortalUrl}/v1/api/portfolio/{accountId}/meta'
    request_7 = requests.get(url=url_7, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_7)) 
    
    url_8 = f'{clientPortalUrl}/v1/api/portfolio/{accountId}/summary'    
    request_8 = requests.get(url=url_8, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_8))             
    
    url_9 = f'{clientPortalUrl}/v1/api/portfolio/{accountId}/ledger'                 
    request_9 = requests.get(url=url_9, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_9)) 
    
    url_10 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/summary/balances'
    request_10 = requests.get(url=url_10, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_10)) 
    
    url_11 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/summary/margins'
    request_11 = requests.get(url=url_11, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_11)) 
    
    url_12 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/summary/market_value'
    request_12 = requests.get(url=url_12, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_12)) 
    
    url_13 = f'{clientPortalUrl}/v1/api/iserver/account/{accountId}/summary/available_funds'    
    request_13 = requests.get(url=url_13, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_13)) 
    
    
#====================================================================================================================
#-------------------------------------------PORTFOLIO ANALYST--------------------------------------------------------
#====================================================================================================================
def portfolioanalyst_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/pa/performance'
    body_1 = {
      "acctIds": [
        accountId
      ],
      "freq": "D"
    }
    request_1 = requests.post(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1))  
    
    
    url_2 = f'{clientPortalUrl}/v1/api/pa/performance'
    body_2 = {
      "acctIds": [
        accountId
      ],
      "conids": [
        265598
      ],
      "currency": "USD",
      "days": 7
    }
    request_2 = requests.post(url=url_2, headers=CPAPI_headers, json=body_2)                      
    print(formatted_HTTPrequest(request_2))  
    
#====================================================================================================================
#-------------------------------------------SCANNER-----------------------------------------------------------------
#====================================================================================================================
def scanner_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/scanner/params'
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  

    url_2 = f'{clientPortalUrl}/v1/api/iserver/scanner/run'
    body_2 = {
            "instrument": "STK",
            "location": "STK.US",
            "type": "TOP_OPEN_PERC_GAIN",
            "filter": [
                {
                    "code":"priceAbove",
                    "value":20
                },
                {
                    "code":"usdVolumeAbove",
                    "value":100000
                }
            ]
    }
    request_2 = requests.post(url=url_2, headers=CPAPI_headers, json=body_2)                      
    print(formatted_HTTPrequest(request_2)) 
    
    
#====================================================================================================================
#-------------------------------------------SUPPRESS-----------------------------------------------------------------
#====================================================================================================================
def suppress_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/questions/suppress'
    body_1 = {
      "messageIds":["o451","o163"]
    }    
    request_1 = requests.post(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1)) 

    # url_2 = f'{clientPortalUrl}/v1/api/iserver/questions/suppress/reset'
    # request_2 = requests.post(url=url_2, headers=CPAPI_headers)                      
    # print(formatted_HTTPrequest(request_2)) 


#====================================================================================================================
#-------------------------------------------WATCHLISTS---------------------------------------------------------------
#====================================================================================================================
def watchlist_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/iserver/watchlist' 
    body_1 = {
      "id":"12345",
      "name":"Test Watchlist",
      "rows":[
        {"C":8314},
        {"C":8894}
      ]
    }    
    request_1 = requests.post(url=url_1, headers=CPAPI_headers, json=body_1)                      
    print(formatted_HTTPrequest(request_1)) 
    
    url_2 = f'{clientPortalUrl}/v1/api/iserver/watchlists' 
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2)) 
    
    url_3 = f'{clientPortalUrl}/v1/api/iserver/watchlist?id=12345' 
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3)) 
    
    url_4 = f'{clientPortalUrl}/v1/api/iserver/watchlist?id=12354' 
    request_4 = requests.delete(url=url_4, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_4)) 
    

#====================================================================================================================
#-------------------------------------------FORECASTEX---------------------------------------------------------------
#====================================================================================================================
def forecastex_endpoints(bearer_token, CPAPI_headers):
    url_1 = f'{clientPortalUrl}/v1/api/forecast/category/tree' 
    request_1 = requests.get(url=url_1, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_1))  
    
    url_2 = f'{clientPortalUrl}/v1/api/forecast/contract/market?underlyingConid=712856720&exchange=FORECASTX'
    request_2 = requests.get(url=url_2, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_2))  
    
    url_3 = f'{clientPortalUrl}/v1/api/forecast/contract/rules?conid=796056361'
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3)) 
    
    url_4 = f'{clientPortalUrl}/v1/api/forecast/contract/schedules?conid=796056361'
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3)) 

    url_5 = f'{clientPortalUrl}/v1/api/forecast/contract/details?conid=796056361'
    request_3 = requests.get(url=url_3, headers=CPAPI_headers)                      
    print(formatted_HTTPrequest(request_3))  
    

#====================================================================================================================
#-------------------------------------------ADD CLEAN FORMATTING-----------------------------------------------------
#==================================================================================================================== 
RESP_HEADERS_TO_PRINT = ["Cookie", "Cache-Control", "Content-Type", "Host"]

def formatted_HTTPrequest(resp: requests.Response) -> str:
    """Print request and response legibly."""
    req = resp.request
    rqh = '\n'.join(f"{k}: {v}" for k, v in req.headers.items())
    rqh = rqh.replace(', ', ',\n    ')
    rqb = req.body if req.body else ""
    
    try:
        rsb = f"\n{pprint.pformat(resp.json())}\n" if resp.text else ""
    except json.JSONDecodeError:
        rsb = resp.text
    rsh = '\n'.join([f"{k}: {v}" for k, v in resp.headers.items() if k in RESP_HEADERS_TO_PRINT])
    
    return_str = '\n'.join([
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
    ])
    time.sleep(1)
    print("")
    return return_str      
    
#====================================================================================================================
#-------------------------------------------MAIN FUNCTION------------------------------------------------------------
#====================================================================================================================
if __name__ == "__main__":
    CPAPI_headers = {"Authorization": "Bearer "+BearerToken}
    CPAPI_headers["User-Agent"] = "python/3.11"
    CPAPI_headers["Cookie"] = f"api={SessionToken}"
    
    ##### CP API requests #####
    session_endpoints(BearerToken, CPAPI_headers)
    # account_endpoints(BearerToken, CPAPI_headers)
    # alerts_endpoints(BearerToken, CPAPI_headers)
    # contract_endpoints(BearerToken, CPAPI_headers)
    # financialadvisor_endpoints(BearerToken, CPAPI_headers)
    # forecastex_endpoints(BearerToken, CPAPI_headers)
    # futuresoptionchain_endpoints(BearerToken, CPAPI_headers)
    # marketdata_endpoints(BearerToken, CPAPI_headers)
    # optionchain_endpoints(BearerToken, CPAPI_headers)
    # orders_endpoints(BearerToken, CPAPI_headers)
    # ordermonitoring_endpoints(BearerToken, CPAPI_headers)
    # portfolio_endpoints(BearerToken, CPAPI_headers)                          
    # portfolioanalyst_endpoints(BearerToken, CPAPI_headers)
    # scanner_endpoints(BearerToken, CPAPI_headers)
    # suppress_endpoints(BearerToken, CPAPI_headers)
    # watchlist_endpoints(BearerToken, CPAPI_headers)
