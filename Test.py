import time
import hmac
import hashlib
import requests

api_key = "OGBOEldJ4ZZ5n8FnTW"
api_secret = "3RZT7NNpZ7wXXRNXAOCFplqddD3Z0mSArY3O"

timestamp = str(int(time.time() * 1000))
recv_window = "5000"

payload = timestamp + api_key + recv_window

signature = hmac.new(
    api_secret.encode(),
    payload.encode(),
    hashlib.sha256
).hexdigest()

headers = {
    "X-BAPI-API-KEY": api_key,
    "X-BAPI-SIGN": signature,
    "X-BAPI-TIMESTAMP": timestamp,
    "X-BAPI-RECV-WINDOW": recv_window
}

url = "https://api-testnet.bybit.com/v5/account/wallet-balance"

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)
