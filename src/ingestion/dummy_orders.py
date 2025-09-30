import pandas as pd
import random

pd.set_option('display.max_columns', None)
def generate_dummy_orders( products_csv,output_csv, num_orders=200, min_basket=4, max_basket=8, price_band=0.4):


    # ---------- Load products ----------
    products = pd.read_csv(products_csv)

    print("products head")
    print(products.head())
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
            anchor_basecat = anchor["base_category"]
            anchor_material = anchor["material"]
            anchor_color = anchor["color"]

            # Candidates: same material, different baseCategory, price in band
            candidates = products[
                (products["id"] != pid) &
                (products["material"] == anchor_material) &
                (products["base_category"] != anchor_basecat) &
                (products["color"] == anchor_color) &
                (products["price"].between(anchor_price * (1 - price_band),
                                           anchor_price * (1 + price_band)))
            ]

            if candidates.empty:
                # fallback: ignore price band
                candidates = products[
                    (products["id"] != pid) &
                    (products["material"] == anchor_material) &
                    (products["base_category"] != anchor_basecat)&
                    (products["color"] == anchor_color)
                ]

            if candidates.empty:
                # last fallback: any product except anchor
                candidates = products[products["id"] != pid]

            chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
            basket = [pid] + chosen

            for item in basket:
                row = products.loc[products["id"] == item].iloc[0]
                orders.append({
                    "order_id": order_id,
                    "product_id": item,
                    "product_name": row["name"],
                    "base_category": row["base_category"],
                    "material": row["material"]
                })
            order_id += 1

    # ---------- Step 2: Generate additional random orders ----------
    while order_id < 1 + num_orders:
        basket_size = random.randint(min_basket, max_basket)
        anchor = products.sample(1).iloc[0]
        anchor_price = anchor["price"]
        anchor_material = anchor["material"]
        anchor_basecat = anchor["base_Category"]

        candidates = products[
            (products["id"] != anchor["id"]) &
            (products["material"] == anchor_material) &
            (products["base_category"] != anchor_basecat) &
            (products["price"].between(anchor_price * (1 - price_band),
                                       anchor_price * (1 + price_band)))
        ]

        if candidates.empty:
            candidates = products[
                (products["id"] != anchor["id"]) &
                (products["material"] == anchor_material) &
                (products["base_category"] != anchor_basecat)
            ]

        if candidates.empty:
            candidates = products[products["id"] != anchor["id"]]

        chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
        basket = [anchor["id"]] + chosen

        for item in basket:
            row = products.loc[products["id"] == item].iloc[0]
            orders.append({
                "order_id": order_id,
                "product_id": item,
                "product_name": row["name"],
                "base_category": row["base_category"],
                "material": row["material"]
            })
        order_id += 1

    orders_df = pd.DataFrame(orders)

    if output_csv:
        orders_df.to_csv(output_csv, index=False)

    return orders_df
