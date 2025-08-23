import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://srikrishnapearls.com/wp-json/wc/v3/orders"
CONSUMER_KEY = os.getenv("WOO_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("WOO_CONSUMER_SECRET")


def fetch_orders():
    orders = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0 Safari/537.36",
        "Accept": "application/json"
    }

    # Last 12 months
    after_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S")

    while True:
        params = {
            "per_page": 100,
            "page": page,
            "status": "completed",
            "after": after_date,
            "consumer_key": CONSUMER_KEY,
            "consumer_secret": CONSUMER_SECRET
        }

        r = requests.get(BASE_URL, params=params, headers=headers)

        print(f"--- PAGE {page} ---")
        print(f"Status Code: {r.status_code}")

        if r.status_code != 200:
            raise Exception(f"Failed to fetch orders: {r.status_code}, {r.text}")

        try:
            data = r.json()
        except ValueError:
            print("Invalid JSON response! Check raw output above.")
            break

        if not data:
            break

        orders.extend(data)
        page += 1

    # Flatten line items
    rows = []
    for order in orders:
        order_id = order.get('id')
        order_date = order.get('date_created')
        line_items = order.get('line_items', [])
        for item in line_items:
            product_id = item.get('product_id')
            if not product_id:
                continue   # skip invalid line_items

            quantity = item.get('quantity', 1)
            line_total = float(item.get('total',0))
            rows.append({
                "order_id": order_id,
                "order_date": order_date,
                "product_id": product_id,
                "quantity": quantity,
                "line_total": line_total
            })

    df = pd.DataFrame(rows)
    df.to_csv("orders_cache.csv", index=False)

    print(f"Total orders fetched: {len(df)}")
    return df


if __name__ == "__main__":
    df = fetch_orders()
    print(df.head())
