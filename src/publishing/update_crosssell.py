import requests
import os

API_URL = "https://srikrishnapearls.com/wp-json/skp-fbt/v1/save-recommendations"
CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")

def save_recommendations(recommendations):
    for row in recommendations:
        payload = {
            "product_id": row["product_id"],
            "recommendations": row["recs"]
        }
        r = requests.post(
            API_URL,
            json=payload,
            auth=(CONSUMER_KEY, CONSUMER_SECRET)
        )
        print(r.status_code, r.text)
