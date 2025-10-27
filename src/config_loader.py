import os
import requests
import time

WP_API_URL = os.getenv("WOO_URL")

def load_config():
    headers = {
        "Accept": "application/json",
        "User-Agent": "SKP-FBT-Batch/1.0 (+https://srikrishnanew-staging.us23.cdn-alpha.com)",
    }
    params = {"_": int(time.time())}  
    try:
        resp = requests.get(WP_API_URL, headers=headers, timeout=10, params=params)
        resp.raise_for_status()  # Raise exception for non-200
        config = resp.json()
    except requests.exceptions.Timeout:
        print("Config fetch timeout! Using defaults...")
        config = {"min_cooccurrence": 1, "top_n": 1 ,"price_band": 40}  # fallback
    except requests.exceptions.RequestException as e:
        print(f"Error fetching config: {e}")
        config = {"min_cooccurrence": 1, "top_n": 1 ,"price_band": 40}  # fallback

    return config

