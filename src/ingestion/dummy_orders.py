import pandas as pd
import random

def generate_dummy_orders(products_csv, output_csv, num_orders=200, min_basket=4, max_basket=8, price_band=0.4):
    """
    Generate dummy orders based on products cache CSV.
    
    Parameters:
    -----------
    products_csv : str
        Path to products CSV file.
    num_orders : int
        Number of orders to generate.
    min_basket : int
        Minimum number of products per order.
    max_basket : int
        Maximum number of products per order.
    price_band : float
        Allowed price variation for products in same order (±price_band).
    output_csv : str or None
        If provided, saves the output CSV to this path. If None, does not save.
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns ['order_id', 'product_id']
    """
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
            candidates = products[
                (products["categories"] == category) &
                (products["id"] != pid) &
                (products["price"].between(anchor_price * (1 - price_band),
                                           anchor_price * (1 + price_band)))
            ]

            if candidates.empty:
                candidates = products[products["id"] != pid]  # fallback

            chosen = random.sample(list(candidates["id"]), min(basket_size - 1, len(candidates)))
            basket = [pid] + chosen

            for item in basket:
                orders.append({"order_id": order_id, "product_id": item})
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
            orders.append({"order_id": order_id, "product_id": item})
        order_id += 1

    orders_df = pd.DataFrame(orders)

    if output_csv:
        orders_df.to_csv(output_csv, index=False)

    return orders_df
