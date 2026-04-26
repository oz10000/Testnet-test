import requests

url = "https://api-testnet.bybit.com/v5/market/time"

try:
    response = requests.get(url, timeout=5)
    print("Status:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error:", e)
