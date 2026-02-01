import os
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("ZOHO_BASE_URL")

print(BASE_URL)

def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"
    params = {
        "refresh_token": os.getenv("ZOHO_REFRESH_TOKEN"),
        "client_id": os.getenv("ZOHO_CLIENT_ID"),
        "client_secret": os.getenv("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token"
    }

    res = requests.post(url, params=params)

    print("STATUS:", res.status_code)
    print("RAW RESPONSE:", res.text)   # 👈 VERY IMPORTANT

    if res.status_code != 200 or not res.text:
        raise Exception("Zoho OAuth returned empty or invalid response")

    data = res.json()

    if "access_token" not in data:
        raise Exception(f"Zoho OAuth failed: {data}")

    return data["access_token"]



def zoho_request(method, endpoint, payload=None, params=None):
    token = get_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}{endpoint}"
    response = requests.request(
        method,
        url,
        headers=headers,
        json=payload,
        params=params
    )
    response.raise_for_status()
    return response.json()
