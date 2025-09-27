import pandas as pd
import random

def generate_dummy_orders(products_csv, output_csv, num_orders=200, min_basket=4, max_basket=8, price_band=0.4):
  # Anchor keyword → complementary categories
    complement_map = {
    # Necklaces → add earrings, bangles, bracelets
    "Necklace": [
        "Pearl Bracelet", "Pearl Studs Earrings", "Pearl Bangle", 
        "Choker Set", "Rani Haar", "Three Line Pearl Necklace set"
    ],
    
    # Rings → add earrings, bracelets
    "Ring": [
        "Precious Stones Studs", "Fancy Pearl Set", "Pearl Bangle"
    ],
    
    # Earrings → add necklaces, bangles
    "Earrings": [
        "Pearl Necklace Sets", "Choker Set", "Pearl Bracelet"
    ],
    
    # Bracelets / Bangles → add necklace, earrings
    "Bracelet": [
        "Pearl Necklace Sets", "Pearl Studs Earrings", "Choker Set"
    ],
    
    # Sets → mix of necklaces + earrings + bangles
    "Set": [
        "Pearl Necklace Sets", "Pearl Bangle", "Pearl Studs Earrings", "Choker Set", "Rani Haar"
    ],
    "Choker Set": [
        "Pearl Bracelet", "Pearl Studs Earrings", "Pearl Bangle"
    ],
    
    # Precious stones → add complementary sets
    "Ruby": ["Pearl Necklace Sets", "Precious Stones Studs"],
    "Emerald": ["Pearl Necklace Sets", "Precious Stones Studs"]
    }


    # ---------- Load products ----------
    products = pd.read_csv(products_csv)
    products = products[
        (products["status"] == "publish") &
        (products["stock_status"] == "instock") &
        (products["catalog_visibility"] == "visible")
    ].copy()
    products["price"] = products["price"].astype(float)

    if products.empty:
        raise ValueError("No valid products found in CSV!")

    orders = []
    order_id = 1001

    # ---------- Step 1: Ensure each product appears at least twice ----------
    for pid in products["id"].unique():
        for _ in range(2):
            basket_size = random.randint(min_basket, max_basket)
            anchor = products[products["id"] == pid].iloc[0]
            anchor_price = anchor["price"]
            category = anchor["categories"]

            # Candidates in same category & price band
            candidates_categories = []
            for keyword, comps in complement_map.items():
                if keyword.lower() in category.lower():
                    candidates_categories = comps
                    break

            if candidates_categories:
            # Use complementary categories
                candidates = products[
                    (products["categories"].isin(candidates_categories)) &
                    (products["id"] != pid) &
                    (products["price"].between(anchor_price*(1-price_band),
                                               anchor_price*(1+price_band)))
                ]
            else:
                # Default: same category + price band
                candidates = products[
                    (products["categories"] == category) &
        (products["id"] != pid) &
        (products["price"].between(anchor_price*(1-price_band),
                                   anchor_price*(1+price_band)))
    ]


            if candidates.empty:
                candidates = products[products["id"] != pid]  # fallback

            chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
            basket = [pid] + chosen

            for item in basket:
                product_name = products.loc[products["id"] == item, "name"].values[0]
                orders.append({
                "order_id": order_id,
                "product_id": item,
                "product_name": product_name
            })
            order_id += 1

    # ---------- Step 2: Generate additional random orders ----------
    while order_id < 1 + num_orders:
        basket_size = random.randint(min_basket, max_basket)
        anchor = products.sample(1).iloc[0]
        anchor_price = anchor["price"]
        category = anchor["categories"]

        candidates = products[
            (products["categories"] == category) &
            (products["id"] != anchor["id"]) &
            (products["price"].between(anchor_price * (1 - price_band),
                                       anchor_price * (1 + price_band)))
        ]
        if candidates.empty:
            candidates = products[products["id"] != anchor["id"]]

        chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
        basket = [anchor["id"]] + chosen

        for item in basket:
           orders.append({
        "order_id": order_id,
        "product_id": item,
        "product_name": product_name
    })
        order_id += 1

    orders_df = pd.DataFrame(orders)

    if output_csv:
        orders_df.to_csv(output_csv, index=False)

    return orders_df
