import time
import hmac
import hashlib
import requests
import os

# =========================
# CONFIGURACIÓN
# =========================

BASE_URL = "https://api-testnet.bybit.com"

API_KEY = os.getenv("BYBIT_API_KEY", "")
API_SECRET = os.getenv("BYBIT_API_SECRET", "")

# =========================
# TEST 1: CONEXIÓN PÚBLICA
# =========================

def test_public():
    print("=== PUBLIC ENDPOINT TEST ===")
    url = f"{BASE_URL}/v5/market/time"

    try:
        r = requests.get(url, timeout=5)
        print("Status:", r.status_code)
        print("Response:", r.text)
    except Exception as e:
        print("Error:", e)

# =========================
# TEST 2: ENDPOINT PRIVADO
# =========================

def sign_request(timestamp, recv_window, query_string=""):
    payload = f"{timestamp}{API_KEY}{recv_window}{query_string}"
    signature = hmac.new(
        API_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def test_private():
    print("=== PRIVATE ENDPOINT TEST ===")

    if not API_KEY or not API_SECRET:
        print("⚠️ API KEY o SECRET no configurados")
        return

    endpoint = "/v5/account/wallet-balance"
    url = BASE_URL + endpoint

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"
    query = "accountType=UNIFIED"

    signature = sign_request(timestamp, recv_window, query)

    headers = {
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(url + "?" + query, headers=headers, timeout=5)
        print("Status:", r.status_code)
        print("Response:", r.text)
    except Exception as e:
        print("Error:", e)

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("=== BYBIT TESTNET CHECK START ===\n")

    test_public()
    print()

    test_private()
    print()

    print("=== END ===")
