import pandas as pd
import itertools
from collections import defaultdict

# --- CONFIG ---
MIN_CO_OCCURRENCE = 3
TOP_N = 3
PRICE_BAND = 40  # ±40%


# --- SIMILARITY LOGIC ---
def build_similarity(baskets: pd.DataFrame, config, products_csv) -> pd.DataFrame:
    """
    Build co-occurrence matrix, compute support, lift, and score.
    """
    print("this is config", config)
    MIN_CO_OCCURRENCE = int(config.get("min_occurrence"))
    TOP_N = int(config.get("top_n"))
    price = int(config.get("price_band"))
    PRICE_BAND = price / 100

    print("MIN_CO_OCCURRENCE", MIN_CO_OCCURRENCE)
    print("TOP_N", TOP_N)
    print("PRICE_BAND", PRICE_BAND)

    co_matrix = defaultdict(lambda: defaultdict(int))
    product_count = defaultdict(int)
    total_baskets = len(baskets)

    # Count co-occurrences & product occurrences
    for products in baskets["products"]:
        unique_products = [p for p in set(products) if p]
        for p in unique_products:
            product_count[p] += 1
        for p1, p2 in itertools.combinations(unique_products, 2):
            co_matrix[p1][p2] += 1
            co_matrix[p2][p1] += 1

    # Compute score and flatten
    rows = []
    pair_count = 0
    for p1, related in co_matrix.items():
        for p2, co_count in related.items():
            if co_count < MIN_CO_OCCURRENCE:
                continue  # min co-occurrence filter

            support_pair = co_count / total_baskets
            support_p1 = product_count[p1] / total_baskets
            support_p2 = product_count[p2] / total_baskets
            lift = support_pair / (support_p1 * support_p2)
            score = 0.7 * lift + 0.3 * support_pair
            rows.append({
                "product_id": p1,
                "other_product": p2,
                "score": score,
                "co_count": co_count
            })
            if p1 < p2 and co_count > MIN_CO_OCCURRENCE:
                pair_count += 1

    print(f"Total unique product pairs with co-occurrence >= {MIN_CO_OCCURRENCE}: {pair_count}")
    similarity_df = pd.DataFrame(rows)

    # --- Type correction for safety ---
    similarity_df["product_id"] = pd.to_numeric(similarity_df["product_id"], errors="coerce").astype("Int64")
    similarity_df["other_product"] = pd.to_numeric(similarity_df["other_product"], errors="coerce").astype("Int64")

    print("Sample similarity_df after build_similarity:")
    print(similarity_df.head())
    return similarity_df


def apply_filters(similarity_df: pd.DataFrame, products_df: pd.DataFrame,
                  price_band=PRICE_BAND, top_n=TOP_N, debug_csv_path=None) -> pd.DataFrame:
    """
    Apply stock, price, and category affinity filters and exclude same base_category pairs.
    Optionally save human-readable recs for debugging.
    """
    if similarity_df.empty:
        print("⚠️ Similarity dataframe is empty — skipping filters.")
        return similarity_df

    # --- Align column types before merging ---
    products_df["id"] = pd.to_numeric(products_df["id"], errors="coerce").astype("Int64")
    similarity_df["product_id"] = pd.to_numeric(similarity_df["product_id"], errors="coerce").astype("Int64")
    similarity_df["other_product"] = pd.to_numeric(similarity_df["other_product"], errors="coerce").astype("Int64")
    
    
    
    
    
    print("✅ Type check before merge:")
    print(similarity_df.dtypes[["product_id", "other_product"]])
    print(products_df.dtypes[["id"]])

    # --- Merge product info for base and recommended ---
    similarity_df = similarity_df.merge(
        products_df[['id', 'name', 'categories', 'price',
                     'stock_status', 'catalog_visibility', 'status']],
        left_on='product_id', right_on='id', suffixes=('', '_base')
    )

    similarity_df = similarity_df.merge(
        products_df[['id', 'name', 'categories', 'price',
                     'stock_status', 'catalog_visibility', 'status']],
        left_on='other_product', right_on='id', suffixes=('', '_rec')
    )

   
    # --- Sort & select top-N ---
    similarity_df = similarity_df.sort_values(['product_id', 'score'], ascending=[True, False])
    top_recs = similarity_df.groupby('product_id').head(top_n).reset_index(drop=True)

    # --- Save for debugging (optional) ---
    if debug_csv_path:
        debug_df = top_recs[[
            'product_id', 'name',
            'other_product', 'name_rec', 'score'
        ]]
        debug_df.to_csv(debug_csv_path, index=False)
        print(f"🧾 Saved debug recommendations to {debug_csv_path}")

    print("✅ Top recommendations (after filters):")
    print(top_recs.head())

    return top_recs[['product_id', 'other_product', 'score']]


def recommend_for_product(similarity_df: pd.DataFrame, product_id: int) -> pd.DataFrame:
    """Return top-N recommendations for a given product."""
    return similarity_df[similarity_df['product_id'] == product_id].reset_index(drop=True)
