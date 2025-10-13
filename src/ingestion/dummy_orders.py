import pandas as pd
import random
import os
from itertools import combinations
from collections import Counter

def generate_dummy_orders(products_csv, output_csv, config, min_basket=3, max_basket=8):
    
    
    
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

    orders = []
    order_id = 1001
    all_pairs = []



    # --- Get same-color, same-material, different-category candidates ---
    def get_candidates(anchor, pid):
        candidates = products[
            (products["id"] != pid) &
            (products["color"] == anchor["color"]) &
            (products["material"] == anchor["material"]) &
            (~products["base_category"].eq(anchor["base_category"]))
            
        ].copy()
        if(pid == 3488):
                print(f"✅DEBUG >> Candidates for product {pid} ({anchor['name']}):")
                print(candidates)
        
        # If too few candidates, relax color constraint
        if len(candidates) < 2:
            
            relaxed_by_color = products[
                (products["id"] != pid) &
                (products["material"] == anchor["material"]) &
                (~products["base_category"].eq(anchor["base_category"]))
            ]
            candidates = pd.concat([candidates, relaxed_by_color]).drop_duplicates(subset=["id"])
            
        if(pid == 3488):
                print(f"💡DEBUG >> Candidates for product {pid} ({anchor['name']}):")
                print(candidates)
        
        

        
        if(candidates["base_category"].nunique()>=2):
            candidates = candidates.sample(frac=1).reset_index(drop=True)
            candidates = candidates.drop_duplicates(subset=["base_category"])

        return candidates


    product_ids = list(products["id"].unique())

    for pid in product_ids:
        for _ in range(4):
            anchor = products.loc[products["id"] == pid].iloc[0]
            candidates = get_candidates(anchor, pid)
            
           
            if candidates.empty:
                continue
            
            if(pid == 3488):
                print(f"💡DEBUG >> Candidates for product {pid} ({anchor['name']}):")
                print(candidates)

            basket_size = random.randint(min_basket, max_basket)
            chosen = []

            used_categories = {anchor["base_category"]}
            for _, row in candidates.iterrows():
                if row["base_category"] not in used_categories:
                    chosen.append(row["id"])
                    used_categories.add(row["base_category"])
                if len(chosen) >= basket_size - 1:
                    break

            if not chosen:
                continue

            basket = [pid] + chosen

            # Save orders
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

            # Collect all possible product pairs
            for a, b in combinations(basket, 2):
                all_pairs.append(tuple(sorted([a, b])))

            order_id += 1

    # --- Keep only pairs that appear at least 3 times ---
    pair_counts = Counter(all_pairs)
    valid_pairs = {pair for pair, count in pair_counts.items() if count >= 3}

    # Build filtered pairs DataFrame
    valid_pairs_list = []
    for a, b in valid_pairs:
        prod_a = products.loc[products["id"] == a].iloc[0]
        prod_b = products.loc[products["id"] == b].iloc[0]
        valid_pairs_list.append({
            "product_id": a,
            "product_name": prod_a["name"],
            "rec_id": b,
            "rec_name": prod_b["name"]
        })

    # --- Save CSVs ---
    orders_df = pd.DataFrame(orders)
    print(orders_df.head())
    pairs_df = pd.DataFrame(valid_pairs_list)

    dummy_csv = os.path.join(os.path.dirname(output_csv), "dummy_orders.csv")
    pairs_csv = os.path.splitext(output_csv)[0] + "_pairs.csv"

    orders_df.to_csv(dummy_csv, index=False)
    pairs_df.to_csv(pairs_csv, index=False)

    print(f"✅ Generated {len(orders_df)} order-product rows across {order_id - 1001} orders.")
    print(f"📦 Saved {len(pairs_df)} valid pairs (appeared ≥3 times) to: {pairs_csv}")

    return orders_df
