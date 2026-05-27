import json
import time
import random
import base64
import pprint
from datetime import datetime
from urllib.parse import quote, quote_plus

import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_Cipher
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_Signature
from Crypto.Hash import SHA256, HMAC, SHA1
from cryptography.hazmat.primitives.serialization import load_pem_parameters

# ── Configuration ─────────────────────────────────────────────────────────────
CONSUMER_KEY        = "YOURCONSUMER"
ACCESS_TOKEN        = "ACCESSTOKEN"
ACCESS_TOKEN_SECRET = "ACCESSTOKENSECRET"
PATH_ENCRYPTION_KEY = "/path/to/private_encryption.pem"
PATH_SIGNATURE_KEY  = "/path/to/private_signature.pem"
PATH_DHPARAM        = "/path/to/dhparam.pem"

BASE_URL = "https://api.ibkr.com/v1/api"

# ── Load keys ─────────────────────────────────────────────────────────────────
with open(PATH_ENCRYPTION_KEY, "r") as f:
    encryption_key = RSA.import_key(f.read())

with open(PATH_SIGNATURE_KEY, "r") as f:
    signature_key = RSA.import_key(f.read())

# DH params are not RSA keys — load with the cryptography library instead.
with open(PATH_DHPARAM, "rb") as f:
    _dh_params  = load_pem_parameters(f.read())
    _dh_numbers = _dh_params.parameter_numbers()
    DH_PRIME      = _dh_numbers.p
    DH_GENERATOR  = _dh_numbers.g  # IBKR always uses generator=2

# ── Helpers ───────────────────────────────────────────────────────────────────
# TESTCONS is a shared paper-trading key; all real consumer keys use limited_poa.
REALM = "test_realm" if CONSUMER_KEY == "TESTCONS" else "limited_poa"

session = requests.Session()

_PRINT_HEADERS = {"Content-Type", "Content-Length", "Date", "Set-Cookie"}


def build_oauth_header(params: dict) -> str:
    """Attach realm and format params as an OAuth Authorization header."""
    combined = {**params, "realm": REALM}
    return "OAuth " + ", ".join(f'{k}="{v}"' for k, v in sorted(combined.items()))


def format_http(resp: requests.Response) -> str:
    """Return a human-readable request/response summary."""
    req = resp.request
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


# ── Step 1: Live Session Token (POST /oauth/live_session_token) ───────────────
# DH challenge: generator ^ random mod prime
dh_random    = random.getrandbits(256)
dh_challenge = hex(pow(DH_GENERATOR, dh_random, DH_PRIME))[2:]

# Decrypt the access token secret with the private encryption key (PKCS1v1.5).
# The resulting bytes, as a hex string, are prepended to the OAuth base string.
decrypted_secret = PKCS1_v1_5_Cipher.new(encryption_key).decrypt(
    ciphertext=base64.b64decode(ACCESS_TOKEN_SECRET),
    sentinel=None,
)
prepend = decrypted_secret.hex()

LST_METHOD = "POST"
LST_URL    = f"{BASE_URL}/oauth/live_session_token"

oauth_params = {
    "oauth_consumer_key":       CONSUMER_KEY,
    "oauth_nonce":              hex(random.getrandbits(128))[2:],
    "oauth_timestamp":          str(int(datetime.now().timestamp())),
    "oauth_token":              ACCESS_TOKEN,
    "oauth_signature_method":   "RSA-SHA256",
    "diffie_hellman_challenge": dh_challenge,
}

params_string = "&".join(f"{k}={v}" for k, v in sorted(oauth_params.items()))
# Prepend is placed before method&url&params in the base string per IB spec.
base_string   = f"{prepend}{LST_METHOD}&{quote_plus(LST_URL)}&{quote(params_string)}"

sha256_hash     = SHA256.new(data=base_string.encode("utf-8"))
sig_bytes       = PKCS1_v1_5_Signature.new(signature_key).sign(sha256_hash)
b64_signature   = base64.b64encode(sig_bytes).decode("utf-8")

oauth_params["oauth_signature"] = quote_plus(b64_signature)

headers  = {"Authorization": build_oauth_header(oauth_params), "User-Agent": "python/3.13"}
lst_resp = session.send(requests.Request(LST_METHOD, LST_URL, headers=headers).prepare())
print(format_http(lst_resp))

if not lst_resp.ok:
    raise SystemExit(f"ERROR: /live_session_token failed ({lst_resp.status_code}). Exiting.")

resp_data      = lst_resp.json()
dh_response    = resp_data["diffie_hellman_response"]
lst_signature  = resp_data["live_session_token_signature"]
lst_expiration = resp_data["live_session_token_expiration"]

# ── Compute LST ───────────────────────────────────────────────────────────────
# Shared secret K = B^a mod p  (completing the DH exchange)
K     = pow(int(dh_response, 16), dh_random, DH_PRIME)
hex_K = hex(K)[2:]

if len(hex_K) % 2:          # hex bytes must be two digits each
    hex_K = "0" + hex_K

bytes_K = bytes.fromhex(hex_K)

if len(bin(K)[2:]) % 8 == 0:   # prepend null byte if no sign bit
    bytes_K = bytes(1) + bytes_K

# LST = base64( HMAC-SHA1(key=K, msg=prepend_bytes) )
computed_lst = base64.b64encode(
    HMAC.new(key=bytes_K, msg=bytes.fromhex(prepend), digestmod=SHA1).digest()
).decode("utf-8")

# ── Validate LST ─────────────────────────────────────────────────────────────
# Server sends HMAC-SHA1(key=LST, msg=consumer_key) as the signature to check against.
validation = HMAC.new(
    key=base64.b64decode(computed_lst),
    msg=CONSUMER_KEY.encode("utf-8"),
    digestmod=SHA1,
).hexdigest()

if validation != lst_signature:
    raise SystemExit("ERROR: LST validation failed. Exiting.")

live_session_token = computed_lst
print("Live session token: OK")
print(f"  Expires : {datetime.fromtimestamp(lst_expiration / 1000)}")
print(f"  LST     : {live_session_token}\n")

# ── Step 2: Authenticated request ─────────────────────────────────────────────
# Uncomment one block below.

# Option A — fetch portfolio accounts
method    = "GET"
url       = f"{BASE_URL}/portfolio/accounts"
json_body = None

# Option B — initialize a brokerage session
# method    = "POST"
# url       = f"{BASE_URL}/iserver/auth/ssodh/init"
# json_body = {"publish": True, "compete": True}

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
    key=base64.b64decode(live_session_token),
    msg=base_string.encode("utf-8"),
    digestmod=SHA256,
).digest()

oauth_params["oauth_signature"] = quote_plus(base64.b64encode(hmac_bytes).decode("utf-8"))

headers  = {"Authorization": build_oauth_header(oauth_params), "User-Agent": "python/3.13"}
response = session.send(requests.Request(method, url, headers=headers, json=json_body).prepare())
print(format_http(response))

time.sleep(1)
print(f"LST = {live_session_token}")
