import requests
import os
import json  

API_URL = "https://srikrishnanew-staging.us23.cdn-alpha.com/wp-json/skp-fbt/v1/save-recs"
WC_API_URL = "https://srikrishnanew-staging.us23.cdn-alpha.com/wp-json/wc/v3/products"

CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")

def save_recommendations(recommendations):
    for row in recommendations:
        # --- 1. Send to custom API ---
        payload = {
            "product_id": row["product_id"],
            "rec_id": row["other_product"],  
            "score": row.get("score", 0)     
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        print("\n➡️ Sending payload:", json.dumps(payload))
        try:
            r = requests.post(API_URL, json=payload, headers=headers)
            print(f"Custom API: Product {row['product_id']} → Status: {r.status_code}, Response: {r.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending product {row['product_id']} to custom API: {e}")

        # --- 2. Update WooCommerce cross-sell IDs ---
        payload_wc = {
            "cross_sell_ids": row.get("cross_sell_ids", [row["other_product"]])
        }
        try:
            r_wc = requests.put(
                f"{WC_API_URL}/{row['product_id']}",
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                json=payload_wc,
                 headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                }
            )
            print(f"WooCommerce: Product {row['product_id']} → Status: {r_wc.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error updating WooCommerce cross-sell for {row['product_id']}: {e}")
