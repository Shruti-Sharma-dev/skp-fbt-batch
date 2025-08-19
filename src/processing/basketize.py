# src/processing/basketize.py
def create_baskets(orders_df):
    """
    Convert orders DataFrame into list of baskets.
    Each basket is a list of product_ids in one order.
    """
    baskets = orders_df.groupby('order_id')['product_id'].apply(list).tolist()
    return baskets
