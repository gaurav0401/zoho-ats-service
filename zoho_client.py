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
    
    res=data['access_token']

    print(res)

    return data["access_token"]

print("Access Token",get_access_token())

def zoho_request(method, endpoint, payload=None, params=None):
    token = get_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        
    }
    url = f"{BASE_URL}{endpoint}"

    kwargs = {
        "method": method,
        "url": url,
        "headers": headers,
        "params": params
    }

    #  ONLY attach json body if payload exists
    if payload is not None:
        kwargs["json"] = payload

    response = requests.request(**kwargs)

    print("ZOHO URL:", response.url)
    print("ZOHO STATUS:", response.status_code)
    print("ZOHO RESPONSE TEXT:", response.text)

    response.raise_for_status()
    return response.json()
