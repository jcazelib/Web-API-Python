"""
This script assumes you've already received an SSO BearerToken & SessionToken (enter both under the INPUTS section)
     Certain topics like sbd+{} ssd+{} and sld+{} will require the IBKR Account ID {accountId} be specified
     Certain topics like smd+{} sor+{} and str+{} will require the user to 1st initialize a brokerage (trading-enabled) session via POST /iserver/auth/ssodh/init

The Websocket request to send is specified in line 90:
     ws.send('smd+12087792+{"fields":["84","85","86","88","7219"]}')   
"""

import json, pprint, requests, time, websocket

#====================================================================================================================
#-------------------------------------------INPUTS-------------------------------------------------------------------
#====================================================================================================================
BearerToken = "XXXXX"
SessionToken = "XXXXX"
accountId = "DUXXXX123"

#====================================================================================================================
#------------------------------------------WEBSOCKETS----------------------------------------------------------------
#====================================================================================================================
session_str = '{"session": ' + '"' +  SessionToken+'"}'

def on_open(ws):
    ws.send(session_str)
    time.sleep(1)
    
    print("Opened Connection")
    print("-----------------")
    
    #ws.send(f'sld+{accountId}')
    #ws.send(f'ssd+{accountId}')
    ws.send('smd+12087792+{"fields":["84","85","86","88","7219"]}')                        #Available Market Data fields  - https://www.interactivebrokers.com/campus/ibkr-api-page/cpapi-v1/#market-data-fields 
    ws.send('smd+8314+{"fields":["84","85","86","88","7219"]}')                            
    #ws.send(f'sbd+{accountId}+12087792+IDEALPRO')          
    #ws.send('smh+265598+{"period": "1d","bar": "1min","source": "trades","format": "%o/%c/%h/%l"}')           
      
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
    #     print("smd request = ", smdreq)                                                  #Print the CONID+smd request we're making via Websocket
    
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
        url=f"wss://api.ibkr.com/v1/api/ws?bearer_token={BearerToken}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=["User-Agent: python/3.11"],
        cookie=f"api={SessionToken}"
    )
    ws.run_forever()
