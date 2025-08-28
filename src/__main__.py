from ingestion import orders, products
from processing import basketize, similarity
from publishing import update_crosssell
from ingestion.products import fetch_products
from ingestion.orders import fetch_orders
from ingestion.dummy_orders import generate_dummy_orders
from processing.basketize import create_baskets
from processing.similarity import build_similarity, apply_filters, recommend_for_product
from publishing import update_crosssell

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import log
import pandas as pd
import ast

def main():
    print("Batch job started...")

    # Load from cache CSVs
    
  
    products_df = pd.read_csv("products_cache.csv")
    orders_df = pd.read_csv("orders_cache.csv")


    # orders_df = fetch_orders()
    # products_df = fetch_products()

    print("\n🛍️ Sample Products Loaded Successfully:")
    print(products_df.head())

    print("\n🛍️ Sample Orders Loaded Successfully:")
    print(len(orders_df))
    
    
    dummy_orders_df = generate_dummy_orders(products_df)
    # Create baskets
    baskets_df = create_baskets(dummy_orders_df)
    print("\n🛍️ Sample Baskets Loaded Successfully:")
    print(baskets_df)

    # Build similarity
    similarity_df = build_similarity(baskets_df)
    print("\n🔍 Similarity DF Info:")
    print(similarity_df.shape)
    print(similarity_df.columns)
    print("\n🛍️ Sample Similarity Scores Loaded Successfully:")
    print(similarity_df.head(50))

    merged = similarity_df.merge(products_df, left_on="other_product", right_on="id", how="left", indicator=True)
    print("DEBUG >> merge results")
    print(merged[["product_id", "other_product", "_merge"]].head(20))

    # #Apply filters
    filtered_df = apply_filters(similarity_df, products_df)
    print("\n🛍️ filtered Loaded Successfully:")

    
    
    
    
    recommendations = filtered_df.to_dict(orient="records")
    # print(recommendations)
    

    update_crosssell.save_recommendations(recommendations)

if __name__ == "__main__":
    main()
