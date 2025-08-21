import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://srikrishnapearls.com/wp-json/wc/v3/products"
CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")


def fetch_products():
    products = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36",
        "Accept": "application/json"
    }

    while True:
        params = {
            "per_page": 100,
            "page": page,
            "status": "publish",
            "consumer_key": CONSUMER_KEY,
            "consumer_secret": CONSUMER_SECRET
        }

        r = requests.get(BASE_URL, params=params, headers=headers)

        print(f"--- PAGE {page} ---")
        print(f"Status Code: {r.status_code}")
        print(f"Response Preview: {r.text[:100]}\n")

        if r.status_code != 200:
            raise Exception(f"Failed to fetch products: {r.status_code}, {r.text}")

        try:
            data = r.json()
        except ValueError:
            print("Invalid JSON response! Check raw output above.")
            break

        if not data:
            break

        products.extend(data)
        page += 1

    df = pd.DataFrame(products)
    print(f"Total products fetched: {len(df)}")
    return df


if __name__ == "__main__":
    df = fetch_products()
    print(df.head())
