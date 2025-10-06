import pandas as pd
import random

def generate_dummy_orders(products_csv, output_csv, num_orders=200, min_basket=4, max_basket=8, price_band=0.4):

    products = pd.read_csv(products_csv)

    # Basic filters
    products = products[
        (products["status"] == "publish") &
        (products["stock_status"] == "instock") &
        (products["catalog_visibility"] == "visible")
    ].copy()
    products["price"] = products["price"].astype(float)

    if products.empty:
        raise ValueError("No valid products found in CSV!")

    # ---------- ✅ Normalize key string columns ----------
    for col in ["base_category", "material", "color", "name"]:
        if col in products.columns:
            products[col] = (
                products[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .replace("nan", "")
            )

    orders = []
    order_id = 1001


    # ---------- Step 1: Ensure each product appears at least twice ----------
    for pid in products["id"].unique():
        for _ in range(2):   # min_cooccurrence = 3
            basket_size = random.randint(min_basket, max_basket)
            anchor = products[products["id"] == pid].iloc[0]
            anchor_price = anchor["price"]
            anchor_basecat = anchor["base_category"]
            anchor_material = anchor["material"]
            anchor_color = anchor["color"]

            # Candidates: same material, same color, different category, price band
            candidates = products[
                (products["id"] != pid) &
                (products["material"] == anchor_material) &
                (products["base_category"] != anchor_basecat) &
                (products["color"] == anchor_color) &
                (products["price"].between(anchor_price * (1 - price_band),
                                           anchor_price * (1 + price_band)))
            ]

            # Fallbacks
            if candidates.empty:
                candidates = products[
                    (products["id"] != pid) &
                    (products["material"] == anchor_material) &
                    (products["base_category"] != anchor_basecat) &
                    (products["color"] == anchor_color)
                ]

            if candidates.empty:
                candidates = products[
                    (products["id"] != pid) &
                    (products["base_category"] != anchor_basecat)
                ]

            # Randomly pick candidates to fill basket
            chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
            basket = [pid] + chosen

            for item in basket:
                row = products.loc[products["id"] == item].iloc[0]
                orders.append({
                    "order_id": order_id,
                    "product_id": item,
                    "product_name": row["name"],
                    "base_category": row["base_category"],
                    "material": row["material"],
                    "color": row["color"]
                })
            order_id += 1

    # ---------- Step 2: Additional random orders ----------
    while order_id < 1 + num_orders:
        basket_size = random.randint(min_basket, max_basket)
        anchor = products.sample(1).iloc[0]
        anchor_price = anchor["price"]
        anchor_material = anchor["material"]
        anchor_basecat = anchor["base_category"]
        anchor_color = anchor["color"]

        candidates = products[
            (products["id"] != anchor["id"]) &
            (products["material"] == anchor_material) &
            (products["base_category"] != anchor_basecat) &
            (products["color"] == anchor_color) &
            (products["price"].between(anchor_price * (1 - price_band),
                                       anchor_price * (1 + price_band)))
        ]

        if candidates.empty:
            candidates = products[
                (products["id"] != anchor["id"]) &
                (products["material"] == anchor_material) &
                (products["base_category"] != anchor_basecat) &
                (products["color"] == anchor_color)
            ]

        if candidates.empty:
            candidates = products[
                (products["id"] != anchor["id"]) &
                (products["base_category"] != anchor_basecat)
            ]

        chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
        basket = [anchor["id"]] + chosen

        for item in basket:
            row = products.loc[products["id"] == item].iloc[0]
            orders.append({
                "order_id": order_id,
                "product_id": item,
                "product_name": row["name"],
                "base_category": row["base_category"],
                "material": row["material"],
                "color": row["color"]
            })
        order_id += 1

    orders_df = pd.DataFrame(orders)

    if output_csv:
        orders_df.to_csv(output_csv, index=False)

    return orders_df
