import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://srikrishnanew-staging.us23.cdn-alpha.com/wp-json/wc/v3/products"
CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")


def fetch_products(products_cache):
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
        print(f"--- PAGE {page} --- Status Code: {r.status_code}")

        if r.status_code != 200:
            raise Exception(f"Failed to fetch products: {r.status_code}, {r.text}")

        try:
            data = r.json()
        except ValueError:
            print("Invalid JSON response!")
            break

        if not data:
            break

        products.extend(data)
        page += 1

    df = pd.DataFrame(products)

    # Safe filtering
    df = df[df['status'] == 'publish']
    df = df[df['stock_status'] == 'instock']
    df = df[df['catalog_visibility'] != 'hidden']

    # Ensure columns exist
    for col in ['sku', 'categories', 'parent']:
        if col not in df.columns:
            df[col] = pd.NA
            
    # Flatten categories
    df['categories'] = df['categories'].apply(
        lambda cats: ','.join([c['name'] for c in cats]) if isinstance(cats, list) else ''
    )

    # Safe parent_id
    df['parent_id'] = df['parent'].fillna(df['id'])

    # Flatten SKU (and replace df directly)
    df = df.explode("sku").reset_index(drop=True)

    # Select important columns
    df = df[['id', 'parent_id', 'categories', 'price', 'stock_status', 'catalog_visibility', 'status', 'sku','name']]


    # Save CSV
    df.to_csv(products_cache, index=False)

    # print(f"Total products fetched: {len(df)}")
    return df


