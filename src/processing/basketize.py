# src/processing/basketize.py

import pandas as pd

def create_baskets(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert order data into baskets (transactions).
    
    Input orders_df expected columns:
    [order_id, customer_id, product_id, quantity, total]

    Returns:
    A DataFrame where each row is one order and the products are grouped into a list.
    """
    try:
        # Group products by order_id
        baskets = (
            orders_df.groupby("order_id")["product_id"]
            .apply(list)   # collect product_ids per order
            .reset_index(name="products")
        )

        print("✅ Baskets created successfully:")
        print(baskets.head())
        return baskets

    except Exception as e:
        print(f"❌ Error while creating baskets: {e}")
        return pd.DataFrame()
