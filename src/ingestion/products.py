import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# --- WooCommerce API Setup ---
baseurl = os.getenv("WOO_URL")
API_URL = f"{baseurl}/wp-json/wc/v3/products"
CONSUMER_KEY = os.getenv("WOO_LOCAL_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_LOCAL_CONSUMER_SECRET")


# --- Helper to extract meta fields ---
def extract_meta_field(meta_data, key):
    """Return the value of a meta field from meta_data array"""
    for meta in meta_data:
        if meta["key"] == key:
            return meta["value"]
    return None


def fetch_products(products_cache):
    products = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0",
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

        r = requests.get(API_URL, params=params, headers=headers, timeout=20)
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

        # --- NEW: Extract material, color, base_category ---
        for product in data:
            product['material'] = extract_meta_field(product.get('meta_data', []), 'material')
            product['color'] = extract_meta_field(product.get('meta_data', []), 'color')
            product['base_category'] = extract_meta_field(product.get('meta_data', []), 'base_category')

        products.extend(data)
        page += 1

    df = pd.DataFrame(products)

    # --- Safe filtering ---
    df = df[df['status'] == 'publish']
    df = df[df['stock_status'] == 'instock']
    df = df[df['catalog_visibility'] != 'hidden']

    # --- Ensure important columns exist ---
    for col in ['sku', 'categories', 'parent', 'material', 'color', 'base_category']:
        if col not in df.columns:
            df[col] = pd.NA

    # --- Flatten categories ---
    df['categories'] = df['categories'].apply(
        lambda cats: ','.join([c['name'] for c in cats]) if isinstance(cats, list) else ''
    )

    # --- Safe parent_id ---
    df['parent_id'] = df['parent'].fillna(df['id'])

    # --- Explode SKU if it's a list ---
    df = df.explode("sku").reset_index(drop=True)

    # --- Select only necessary columns ---
    df = df[['id', 'parent_id', 'categories', 'price', 'stock_status',
             'catalog_visibility', 'status', 'sku', 'name',
             'material', 'color', 'base_category']]

    # --- Save CSV ---
    df.to_csv(products_cache, index=False)
    print(f"✅ Total products fetched and saved: {len(df)}")

    return df
