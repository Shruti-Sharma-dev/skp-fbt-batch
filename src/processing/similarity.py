import pandas as pd
import itertools
from collections import defaultdict

# --- CONFIG ---
MIN_CO_OCCURRENCE = 3
TOP_N = 3
PRICE_BAND = 0.4  # ±40%


# --- SIMILARITY LOGIC ---
def build_similarity(baskets: pd.DataFrame) -> pd.DataFrame:
    """
    Build co-occurrence matrix, compute support, lift, and score.
    """
    co_matrix = defaultdict(lambda: defaultdict(int))
    product_count = defaultdict(int)
    total_baskets = len(baskets)

    # Count co-occurrences & product occurrences
    for products in baskets['products']:
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
            rows.append({'product_id': p1, 'other_product': p2, 'score': score, 'co_count': co_count})
            if p1 < p2 and co_count > 3:  # p1 < p2 avoids double counting
                pair_count += 1
    print(f"Total unique product pairs with co-occurrence >= {MIN_CO_OCCURRENCE}: {pair_count}")
    similarity_df = pd.DataFrame(rows)
    print("Sample similarity_df after build_similarity:")
    print(similarity_df.head())
    return similarity_df


def apply_filters(similarity_df: pd.DataFrame, products_df: pd.DataFrame,
                  price_band=PRICE_BAND, top_n=TOP_N) -> pd.DataFrame:
    """
    Apply stock, price, and category affinity filters.
    """
    if similarity_df.empty:
        return similarity_df

    # Merge product info for base and recommended
    similarity_df = similarity_df.merge(
        products_df[['id', 'categories', 'price', 'stock_status', 'catalog_visibility', 'status']],
        left_on='product_id', right_on='id', suffixes=('', '_base')
    )
    similarity_df = similarity_df.merge(
        products_df[['id', 'categories', 'price', 'stock_status', 'catalog_visibility', 'status']],
        left_on='other_product', right_on='id', suffixes=('', '_rec')
    )

    # Filter out-of-stock, hidden, draft safely (case-insensitive)
    similarity_df = similarity_df[
        (similarity_df['stock_status'].str.lower() == 'instock') &
        (similarity_df['status'].str.lower() == 'publish') &
        (similarity_df['catalog_visibility'].str.lower() == 'visible') &
        (similarity_df['stock_status_rec'].str.lower() == 'instock') &
        (similarity_df['status_rec'].str.lower() == 'publish') &
        (similarity_df['catalog_visibility_rec'].str.lower() == 'visible')
    ]
    print("After stock/status/visibility filter:")
    print(similarity_df.head())

    # Price band filter
    similarity_df = similarity_df[
        (similarity_df['price_rec'] >= similarity_df['price'] * (1 - price_band)) &
        (similarity_df['price_rec'] <= similarity_df['price'] * (1 + price_band))
    ]
    print("After price band filter:")
    print(similarity_df.head())

    # # Category affinity filter
    # def affinity_check(row):
    #     base_cat = row['categories']
    #     rec_cat = row['categories_rec']
    #     allowed = CATEGORY_AFFINITY.get(base_cat, [])
    #     return rec_cat in allowed

    # similarity_df = similarity_df[similarity_df.apply(affinity_check, axis=1)]
    # print("After category affinity filter:")
    # print(similarity_df.head())

    # Keep top N recommendations per product
    
    similarity_df = similarity_df.sort_values(['product_id', 'score'], ascending=[True, False])
    top_recs = similarity_df.groupby('product_id').head(top_n).reset_index(drop=True)
    print("Top recs:")
    print(top_recs.head())
    return top_recs[['product_id', 'other_product', 'score']]


def recommend_for_product(similarity_df: pd.DataFrame, product_id: int) -> pd.DataFrame:
    """Return top-N recommendations for a given product."""
    return similarity_df[similarity_df['product_id'] == product_id].reset_index(drop=True)
