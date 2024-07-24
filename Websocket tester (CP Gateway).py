"""
Python script used for testing Websockets via CP API - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#websockets   |   Certain requests like sbd+{} ssd+{} and sld+{} will require the IBKR Account ID {accountId} be included 

This script assumes you've logged into the Client Portal API gateway (either the IBKR Live/Paper account at localhost:5000) and received "Client Login Succeeds"
    Initial set-up instructions - https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#get-started

The Websocket request to send is specified in line 61:
    ws.send('smd+12087792+{"fields":["84","85","86","88","7219"]}')    
"""

import json
import requests
import time
import ssl
import urllib3                                                                               #(Optional) for added cleanliness
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)                          #(Optional) for added cleanliness

#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=--==-INPUTS-==-=-=-===-=-==-=-=-=-----=-=-=-=-==-=-=-====-=-=-====-=-=-==
#====================================================================================================================
baseURL = "localhost:5000"
accountId = "ACCOUNTID"


#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-TICKLE REQUEST=-===-=-==-=-=-=-----=-=-=-=-==-=-=-=-=-=-=-==-===-=-==-=-
#====================================================================================================================
method = 'GET'
url = f'https://{baseURL}/v1/api/tickle'                                                #First make a request to the /tickle endpoint and save the returned session value.

# headers = {}
# headers["User-Agent"] = "python/3.8"                                                  #May not be necessary for all customers

print("-----------REQUEST-----------------------")
print(method, url)
tickle_request = requests.get(url=url, verify=False)
print("")


print("-----------RESPONSE-----------------------")
req_json = json.dumps(tickle_request.json(), indent=2)
print(tickle_request)
print(req_json)
print("")


#====================================================================================================================
#-=-=-=-==---=-=-=-=-======-==-=-=-=-==--=-=-WEBSOCKETS=-===-=-==-=-=-=-----=-=-=-=-==-=-=-=-=-=-=-==-===-=-==-=---==
#====================================================================================================================
import websocket

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
        url=f"wss://{baseURL}/v1/api/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=["User-Agent: python/3.8"],
        cookie=f"api={TICKLE_COOKIE}"
    )
    #ws.run_forever()
    ws.run_forever(sslopt={"cert_reqs":ssl.CERT_NONE})    
    
    
'''
Users without a signed server certificate should pass
> sslopt={"cert_reqs":ssl.CERT_NONE}
as an argument to ws.run_forever()
'''
    
   