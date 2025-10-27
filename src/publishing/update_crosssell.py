import requests
import os
import json  
import dotenv

dotenv.load_dotenv()

    
# Access your variables
base_url = os.getenv("WOO_URL")
products_url = f"{base_url}/wp-json/wc/v3/products"

API_URL = f"{base_url}/wp-json/skp-fbt/v1/save-recs"
WC_API_URL = f"{base_url}/wp-json/wc/v3/products"



CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")

def save_recommendations(grouped_recommendations):
    """
    grouped_recommendations: list of dicts like
    [
      {
        "product_id": 10192,
        "recommendations": [
            {"rec_id": 14710, "score": 9.8011},
            {"rec_id": 8114, "score": 4.6132},
            {"rec_id": 7337, "score": 4.1277}
        ]
      },
      ...
    ]
    """
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    for product in grouped_recommendations:
        product_id = product["product_id"]
        recs = product["recommendations"]

        # --- 1️⃣ Send each product with all recs to custom API ---
        payload = {
            "product_id": product_id,
            "recommendations": recs
        }

        print("\n➡️ Sending payload:", json.dumps(payload))
        try:
            r = requests.post(API_URL, json=payload, headers=headers)
            print(f"Custom API: Product {product_id} → Status: {r.status_code}, Response: {r.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending product {product_id} to custom API: {e}")

        # --- 2️⃣ Update WooCommerce cross-sell IDs ---
        cross_sell_ids = [rec["rec_id"] for rec in recs]
        payload_wc = {"cross_sell_ids": cross_sell_ids}

        try:
            r_wc = requests.put(
                f"{WC_API_URL}/{product_id}",
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                json=payload_wc,
                headers=headers
            )
            print(f"WooCommerce: Product {product_id} → Status: {r_wc.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error updating WooCommerce cross-sell for {product_id}: {e}")
