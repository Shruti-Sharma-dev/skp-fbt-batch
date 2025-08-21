import pandas as pd
from collections import defaultdict
import itertools

def compute_recommendations(baskets_df, products_df, min_cooccurrence=2, top_n=3):
    """
    Compute FBT recommendations using co-occurrence, support, lift, and filters.

    Args:
        baskets_df (pd.DataFrame): columns = ["order_id", "products"] where products is a list of product_ids
        products_df (pd.DataFrame): must have ["product_id", "price", "stock", "status", "category"]
        min_cooccurrence (int): minimum number of baskets where pair must appear
        top_n (int): number of recommendations per product

    Returns:
        dict: { product_id: [recommended_product_ids] }
    """

    total_orders = baskets_df["order_id"].nunique()

    # Step 1: Compute co-occurrence counts
    co_counts = defaultdict(int)
    support_counts = defaultdict(int)

    for _, row in baskets_df.iterrows():
        basket = set(row["products"])
        for item in basket:
            support_counts[item] += 1
        for a, b in itertools.combinations(sorted(basket), 2):
            co_counts[(a, b)] += 1
            co_counts[(b, a)] += 1  # symmetric
    print(support_counts)
    # Step 2: Compute scores
    recs = defaultdict(list)

    for (a, b), co in co_counts.items():
        if co < min_cooccurrence:
            continue

        supp_a = support_counts[a]
        supp_b = support_counts[b]

        pair_support = co / total_orders
        lift = (co / total_orders) / ((supp_a / total_orders) * (supp_b / total_orders))
        score = 0.7 * lift + 0.3 * pair_support

        recs[a].append((b, score))
        print(f"Pair ({a}, {b}) → co={co}, supp_a={supp_a}, supp_b={supp_b}")
        print(f"pair_support={pair_support:.3f}, lift={lift:.3f}, score={score:.3f}")

        for base, candidates in recs.items():
          print(f"{base} → {[c[0] for c in candidates]}")



    # Step 3: Apply filters
    filtered_recs = {}
    for base, candidates in recs.items():
        base_row = products_df.loc[products_df["product_id"] == base]
        if base_row.empty:
            continue

        base_price = base_row["price"].values[0]
        base_category = base_row["category"].values[0]

        # Price guard
        min_price = base_price * 0.6
        max_price = base_price * 1.4

        filtered = []
        for cand, score in candidates:
            row = products_df.loc[products_df["product_id"] == cand]
            if row.empty:
                continue
   
            cand_price = row["price"].values[0]
            cand_stock = row["stock"].values[0]
            cand_status = row["status"].values[0]
            cand_category = row["category"].values[0]

            # # Exclusion filters
            if cand_stock <= 0 or cand_status in ("hidden", "draft"):
                continue
            # if not (min_price <= cand_price <= max_price):
            #     continue
            # if not is_category_compatible(base_category, cand_category):
            #     continue

            filtered.append((cand, score))
            
        for cand, score in candidates:
            print(f"Checking candidate {cand} for base {base} with score {score}")


        # Pick top-N by score
        filtered = sorted(filtered, key=lambda x: x[1], reverse=True)[:top_n]
        filtered_recs[base] = [c for c, _ in filtered]

    return filtered_recs


def is_category_compatible(base_category, cand_category):
    """Apply jewellery category affinity rules"""
    affinity_map = {
        "Necklace": ["Earrings", "Bangles", "Pendants"],
        "Earrings": ["Necklace", "Bangles"],
        "Rings": ["Bracelets", "Earrings"],
        "Bracelets": ["Rings", "Earrings"],
        "Pendants": ["Necklace", "Earrings"],
    }

    if base_category == cand_category:
        return True
    return cand_category in affinity_map.get(base_category, [])
