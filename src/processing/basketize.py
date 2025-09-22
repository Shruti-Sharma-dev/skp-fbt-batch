# src/processing/basketize.py

import pandas as pd

def create_baskets(orders_df: pd.DataFrame) -> pd.DataFrame:
    
    try:
        

        # Group products by order_id
        baskets = (
            orders_df.groupby("order_id")["product_id"]
            .apply(list)   # collect product_ids per order
            .reset_index(name="products")
        )
        
        
        
        # Remove invalid product IDs (0)
        baskets['products'] = baskets['products'].apply(lambda x: [p for p in x if p != 0])

        # Drop orders with empty baskets
        baskets = baskets[baskets['products'].map(len) > 0]

        print("✅ Baskets created successfully:")
        print(baskets.head())
        return baskets

    except Exception as e:
        print(f"❌ Error while creating baskets: {e}")
        return pd.DataFrame()
