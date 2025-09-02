import requests
import os

API_URL = "http://localhost/testplugin/wp-json/skp-fbt/v1/save-recs"
# API_URL = "https://srikrishnanew-staging.us23.cdn-alpha.com/wp-json/skp-fbt/v1/save-recommendations"
CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")

def save_recommendations(recommendations):
   

    for row in recommendations:
        payload = {
            "product_id": row["product_id"],
            "recommendations": row["other_product"],
            "score": row.get("score", 0) 
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            r = requests.post(
                API_URL,
                json=payload,
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                headers=headers
            )
            print(f"Product {row['product_id']} → Status: {r.status_code}, Response: {r.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending product {row['product_id']}: {e}")


