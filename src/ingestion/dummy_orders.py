import pandas as pd
import random
import os

def generate_dummy_orders(products_csv, output_csv, num_orders=200, min_basket=3, max_basket=5):
    products = pd.read_csv(products_csv)

    # --- Basic filters ---
    products = products[
        (products["status"].str.lower() == "publish") &
        (products["stock_status"].str.lower() == "instock") &
        (products["catalog_visibility"].str.lower() == "visible")
    ].copy()
    products["price"] = products["price"].astype(float)

    if products.empty:
        raise ValueError("❌ No valid products found in CSV!")

    # --- Normalize key string columns ---
    for col in ["base_category", "material", "color", "name"]:
        if col in products.columns:
            products[col] = (
                products[col].astype(str)
                .str.strip()
                .str.lower()
                
                .replace("nan", "")
            )

    orders = []
    pairs = []
    order_id = 1001

    # --- Normalize materials ---
    def normalize_material(mat_str):
        return [x.strip().lower() for x in str(mat_str).replace(";", ",").split(",") if x.strip()]

    # --- Get perfect same-material same-color but different-category candidates ---
    def get_candidates(anchor, pid):
        anchor_materials = set(normalize_material(anchor["material"]))
        anchor_color = anchor["color"]
        anchor_cat = anchor["base_category"]

        candidates = products[
            (products["id"] != pid) &
            (products["color"] == anchor_color) &
            products["material"]==anchor["material"] &
            (~products["base_category"].eq(anchor_cat))
        ]

        # Remove duplicates per category
        candidates = candidates.drop_duplicates(subset=["base_category"])
        return candidates

    # --- Generate baskets ---
    product_ids = list(products["id"].unique())
    random.shuffle(product_ids)

    for pid in product_ids:
        anchor = products.loc[products["id"] == pid].iloc[0]
        candidates = get_candidates(anchor, pid)
        if candidates.empty:
            continue

        basket_size = random.randint(min_basket, max_basket)
        chosen = []
        used_categories = {anchor["base_category"]}

        for _, row in candidates.iterrows():
            cat = row["base_category"]
            if cat not in used_categories:
                chosen.append(row["id"])
                used_categories.add(cat)
            if len(chosen) >= basket_size - 1:
                break

        if not chosen:
            continue

        basket = [pid] + chosen

        # --- Save orders ---
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

        # --- Save recommendation pairs ---
        for cid in chosen:
            rec_row = products.loc[products["id"] == cid].iloc[0]
            pairs.append({
                "product_id": pid,
                "product_name": anchor["name"],
                "rec_id": cid,
                "rec_name": rec_row["name"]
            })

        order_id += 1

    # --- Save CSVs ---
    orders_df = pd.DataFrame(orders)
    if output_csv:
        orders_df.to_csv(output_csv, index=False)

    pairs_df = pd.DataFrame(pairs)
    pairs_csv = os.path.splitext(output_csv)[0] + "_pairs.csv"
    pairs_df.to_csv(pairs_csv, index=False)

    print(f"✅ Generated {len(orders_df)} order-product rows across {order_id - 1001} orders.")
    print(f"📦 Saved pairs file: {pairs_csv} with {len(pairs_df)} rows.")

    return orders_df
