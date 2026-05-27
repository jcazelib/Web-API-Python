import json
import random
import base64
import pprint
from datetime import datetime
from urllib.parse import quote, quote_plus

import requests
from Crypto.Hash import SHA256, HMAC

# ── Configuration ─────────────────────────────────────────────────────────────
CONSUMER_KEY       = "YOURCONSUMER"
ACCESS_TOKEN       = "ACCESSTOKEN"
LIVE_SESSION_TOKEN = "LIVESESSIONTOKEN"
ACCOUNT_ID         = "ACCOUNTID"

REALM = "test_realm" if CONSUMER_KEY == "TESTCONS" else "limited_poa"
BASE_URL           = "https://api.ibkr.com/v1/api"

# ── Helpers ───────────────────────────────────────────────────────────────────
session = requests.Session()
_PRINT_HEADERS = {"Content-Type", "Content-Length", "Date", "Set-Cookie"}


def build_oauth_header(params: dict) -> str:
    combined = {**params, "realm": REALM}
    return "OAuth " + ", ".join(f'{k}="{v}"' for k, v in sorted(combined.items()))

def format_http(resp: requests.Response) -> str:
    req         = resp.request
    req_headers = "\n".join(f"{k}: {v}" for k, v in req.headers.items())
    req_headers = req_headers.replace(", ", ",\n    ")
    req_body    = f"\n{pprint.pformat(json.loads(req.body))}\n" if req.body else ""
    try:
        resp_body = f"\n{pprint.pformat(resp.json())}\n" if resp.text else ""
    except json.JSONDecodeError:
        resp_body = resp.text
    resp_headers = "\n".join(
        f"{k}: {v}" for k, v in resp.headers.items() if k in _PRINT_HEADERS
    )
    return "\n".join([
        "─── REQUEST ────────────────────────────────",
        f"{req.method} {req.url}",
        "",
        req_headers,
        req_body,
        "─── RESPONSE ───────────────────────────────",
        f"{resp.status_code} {resp.reason}",
        resp_headers,
        resp_body,
        "",
    ])


# ── Endpoint selection ────────────────────────────────────────────────────────
# Uncomment exactly one method/url/body block.
# Leave body = {} for requests with no payload.
#
# CONID 265598      = AAPL stock
# CONID 12087792    = EUR.USD FX pair
# CONID 11004968    = ES futures index

# ── Session / Auth ────────────────────────────────────────────────────────────
method = "GET"
url    = f"{BASE_URL}/portfolio/accounts"
body   = {}

# method = "GET";  url = f"{BASE_URL}/iserver/accounts";                body = {}
# method = "POST"; url = f"{BASE_URL}/iserver/auth/status";             body = {}
# method = "GET";  url = f"{BASE_URL}/tickle";                          body = {}
# method = "POST"; url = f"{BASE_URL}/logout";                          body = {}

# Initiate brokerage session — https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#ssodh-init
# method = "POST"; url = f"{BASE_URL}/iserver/auth/ssodh/init?publish=true&compete=true"; body = {}
# method = "POST"; url = f"{BASE_URL}/iserver/auth/ssodh/init"; body = {"publish": True, "compete": True}

# ── Account ───────────────────────────────────────────────────────────────────
# method = "GET"; url = f"{BASE_URL}/portfolio/accounts";                        body = {}
# method = "GET"; url = f"{BASE_URL}/portfolio/subaccounts";                     body = {}
# method = "GET"; url = f"{BASE_URL}/portfolio/subaccounts2";                    body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/pnl/partitioned";           body = {}
# method = "GET"; url = f"{BASE_URL}/acesws/{ACCOUNT_ID}/signatures-and-owners"; body = {}

# ── Contract / Security Definition ───────────────────────────────────────────
# method = "GET"; url = f"{BASE_URL}/trsrv/all-conids/?exchange=NYSE";           body = {}  # all CONIDs by exchange
# method = "GET"; url = f"{BASE_URL}/trsrv/secdef?conids=265598";                body = {}
# method = "GET"; url = f"{BASE_URL}/trsrv/stocks?symbols=AAPL,IBKR,IBM";        body = {}
# method = "GET"; url = f"{BASE_URL}/trsrv/futures?symbols=ES";                  body = {}
# method = "GET"; url = f"{BASE_URL}/trsrv/secdef/schedule?assetClass=STK&symbol=AAPL&exchange=NASDAQ&exchangeFilter=NASDAQ"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/contract/265598/info";              body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/contract/265598/info-and-rules?isBuy=true"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/contract/265598/algos?addDescription=1&addParams=1"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/currency/pairs?currency=USD";       body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/exchangerate?source=JPY&target=USD"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/secdef/strikes?conid=265598&sectype=OPT&month=DEC25"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/secdef/info?conid=265598&sectype=OPT&month=DEC25&strike=0&right=C"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/secdef/bond-filters?symbol=BOND&issuerId=e1400715"; body = {}
# method = "POST"; url = f"{BASE_URL}/iserver/secdef/search"; body = {"symbol": "IBM", "name": True, "secType": "STK"}

# ── Options & Futures Chain ───────────────────────────────────────────────────
# Step 1 → POST /iserver/secdef/search
# Step 2 → GET  /iserver/secdef/strikes
# Step 3 → GET  /iserver/secdef/info

# Option chain (AAPL):
# method = "POST"; url = f"{BASE_URL}/iserver/secdef/search"; body = {"symbol": "AAPL", "name": True, "secType": "OPT"}
# method = "GET";  url = f"{BASE_URL}/iserver/secdef/strikes?conid=265598&sectype=OPT&month=DEC25"; body = {}
# method = "GET";  url = f"{BASE_URL}/iserver/secdef/info?conid=265598&sectype=OPT&month=DEC25&strike=0&right=C"; body = {}

# Future option chain (ES) — use the Index CONID 11004968 for steps 2 & 3:
# method = "POST"; url = f"{BASE_URL}/iserver/secdef/search"; body = {"symbol": "ES", "name": True, "secType": "FUT"}
# method = "GET";  url = f"{BASE_URL}/iserver/secdef/strikes?exchange=CME&conid=11004968&sectype=FOP&month=DEC25"; body = {}
# method = "GET";  url = f"{BASE_URL}/iserver/secdef/info?exchange=CME&conid=11004968&sectype=FOP&month=DEC25&strike=0&right=C"; body = {}

# ── Market Data ───────────────────────────────────────────────────────────────
# Snapshot — must be called twice to receive data:
# method = "GET"; url = f"{BASE_URL}/iserver/marketdata/snapshot?conids=12087792@IDEALPRO&since=0&fields=31,55,6509,84"; body = {}

# Historical:
# method = "GET"; url = f"{BASE_URL}/iserver/marketdata/history?conid=12087792&exchange=IDEALPRO&period=1d&bar=1min&outsideRth=false"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/marketdata/history?conid=12087792&exchange=IDEALPRO&period=10d&bar=1d&outsideRth=false";  body = {}

# ── Orders ────────────────────────────────────────────────────────────────────
# Docs: https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#place-order

# Place order:
# method = "POST"
# url    = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/orders"
# body   = {
#     "orders": [{
#         "side": "BUY", "quantity": 1, "conid": 265598,
#         "orderType": "LMT", "listingExchange": "SMART",
#         "price": 1, "tif": "DAY", "outsideRTH": False,
#     }]
# }

# Reply to order confirmation — https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#place-order-reply
# reply_id = "5f8de0bb-a743-4b9e-8439-82686c1a8567"
# method = "POST"; url = f"{BASE_URL}/iserver/reply/{reply_id}"; body = {"confirmed": True}

# What-if order:
# method = "POST"
# url    = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/orders/whatif"
# body   = {"orders": [{"conid": 265598, "orderType": "LMT", "outsideRTH": False, "price": 100, "side": "BUY", "tif": "GTC", "quantity": 1}]}

# Modify order:
# order_id = "ORD123"
# method = "POST"
# url    = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/order/{order_id}"
# body   = {"orders": [{"conid": 265598, "orderType": "LMT", "outsideRTH": False, "price": 1, "side": "BUY", "tif": "GTC", "quantity": 2}]}

# Cancel order:
# order_id = "ORD123"
# method = "DELETE"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/order/{order_id}"; body = {}

# ── Order Monitoring ──────────────────────────────────────────────────────────
# method = "GET"; url = f"{BASE_URL}/iserver/account/orders";                          body = {}  # live orders
# method = "GET"; url = f"{BASE_URL}/iserver/account/order/status/2000983381";         body = {}  # order status
# method = "GET"; url = f"{BASE_URL}/iserver/account/trades";                          body = {}  # executions

# WebSocket order updates — https://ibkrcampus.com/ibkr-api-page/cpapi-v1/#ws-order-updates-sub
# URL     : wss://api.ibkr.com/v1/api/ws?oauth_token={ACCESS_TOKEN}
# Message : {"session": "{sessionId from /tickle}"}
# Subscribe: sor+{}

# ── Portfolio ─────────────────────────────────────────────────────────────────
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/positions/0";              body = {}  # open positions
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/position/265598";          body = {}  # position by CONID
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/allocation";               body = {}  # allocation by class/industry
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/summary";                  body = {}  # cash & margin
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/ledger";                   body = {}  # cash by currency
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/meta";                     body = {}
# method = "GET"; url = f"{BASE_URL}/portfolio/{ACCOUNT_ID}/positions/invalidate";     body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/summary/balances";   body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/summary/margins";    body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/summary/market_value";    body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/summary/available_funds"; body = {}
# method = "POST"; url = f"{BASE_URL}/portfolio/allocation"; body = {"acctIds": [ACCOUNT_ID]}

# ── Financial Advisor ─────────────────────────────────────────────────────────
# Switch account:
# method = "POST"; url = f"{BASE_URL}/iserver/account"; body = {"acctId": ACCOUNT_ID}

# method = "GET"; url = f"{BASE_URL}/iserver/account/allocation/accounts"; body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/allocation/group";    body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/allocation/presets";  body = {}

# Get allocation group details:
# method = "POST"; url = f"{BASE_URL}/iserver/account/allocation/group/single"; body = {"name": "Group1"}

# Create allocation group (methods: A=AvailableEquity E=Equal N=NetLiq C=CashQty P=Percentages R=Ratios S=Shares):
# method = "POST"; url = f"{BASE_URL}/iserver/account/allocation/group"
# body = {"name": "Group1", "default_method": "E", "accounts": [{"name": "DUXXXX123"}, {"name": "DUXXXX124"}]}

# Create allocation profile:
# method = "POST"; url = f"{BASE_URL}/iserver/account/allocation/group"
# body = {"name": "Profile1", "default_method": "C", "accounts": [{"amount": 2, "name": "DUXXXX123"}, {"amount": 1, "name": "DUXXXX124"}]}

# Delete allocation group:
# method = "POST"; url = f"{BASE_URL}/iserver/account/allocation/group/delete"; body = {"name": "Group1"}

# ── Portfolio Analyst ─────────────────────────────────────────────────────────
# method = "POST"; url = f"{BASE_URL}/pa/performance";   body = {"acctIds": [ACCOUNT_ID], "freq": "D"}
# method = "POST"; url = f"{BASE_URL}/pa/transactions";  body = {"acctIds": [ACCOUNT_ID], "conids": [265598], "currency": "USD", "days": 7}

# ── Scanner ───────────────────────────────────────────────────────────────────
# method = "GET"; url = f"{BASE_URL}/iserver/scanner/params"; body = {}

# method = "POST"; url = f"{BASE_URL}/iserver/scanner/run"
# body = {"instrument": "STK", "location": "STK.US", "type": "TOP_OPEN_PERC_GAIN",
#         "filter": [{"code": "priceBelow", "value": 20}, {"code": "usdVolumeAbove", "value": 100000}]}

# method = "POST"; url = f"{BASE_URL}/hmds/scanner"
# body = {"instrument": "STK", "locations": "STK.US", "scanCode": "TOP_OPEN_PERC_GAIN", "secType": "STK",
#         "filter": [{"code": "priceBelow", "value": 20}, {"code": "usdVolumeAbove", "value": 100000}]}

# ── Suppress / Questions ──────────────────────────────────────────────────────
# method = "POST"; url = f"{BASE_URL}/iserver/questions/suppress";       body = {"messageIds": ["o451", "o163"]}
# method = "POST"; url = f"{BASE_URL}/iserver/questions/suppress/reset"; body = {}

# ── Alerts ────────────────────────────────────────────────────────────────────
# method = "GET"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/alerts";              body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/alert/1132135167?type=Q";          body = {}
# method = "GET"; url = f"{BASE_URL}/iserver/account/mta";                              body = {}

# Create alert — body schema: https://github.com/awiseib/Python-CPAPI-Library/tree/main/Alerts
# method = "POST"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/alert"; body = {...}

# Activate/deactivate alert (alertActive: 1=active, 0=inactive):
# method = "POST"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/alert/activate"; body = {"alertId": 2051736314, "alertActive": 0}

# Delete alert:
# method = "DELETE"; url = f"{BASE_URL}/iserver/account/{ACCOUNT_ID}/alert/1132135167"; body = {}


# ── OAuth 1.0a signing (HMAC-SHA256 with LST as key) ─────────────────────────

oauth_params = {
    "oauth_consumer_key":     CONSUMER_KEY,
    "oauth_nonce":            hex(random.getrandbits(128))[2:],
    "oauth_signature_method": "HMAC-SHA256",
    "oauth_timestamp":        str(int(datetime.now().timestamp())),
    "oauth_token":            ACCESS_TOKEN,
}

params_string = "&".join(f"{k}={v}" for k, v in sorted(oauth_params.items()))
base_string   = f"{method}&{quote_plus(url)}&{quote(params_string)}"

hmac_bytes = HMAC.new(
    key=base64.b64decode(LIVE_SESSION_TOKEN),
    msg=base_string.encode("utf-8"),
    digestmod=SHA256,
).digest()

oauth_params["oauth_signature"] = quote_plus(base64.b64encode(hmac_bytes).decode("utf-8"))

headers = {
    "Authorization": build_oauth_header(oauth_params),
    "User-Agent":    "python/3.13",
}

# ── Send request ──────────────────────────────────────────────────────────────

request  = requests.Request(method, url, headers=headers, json=body if body else None)
response = session.send(request.prepare())
print(format_http(response))
