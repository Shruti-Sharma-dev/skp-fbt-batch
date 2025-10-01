from ingestion import orders, products, add_base
from processing import basketize, similarity
from publishing import update_crosssell
from ingestion.products import fetch_products
from ingestion.orders import fetch_orders
from ingestion.dummy_orders import generate_dummy_orders
from processing.basketize import create_baskets
from processing.similarity import build_similarity, apply_filters, recommend_for_product
from publishing import update_crosssell


from config_loader import load_config, WP_API_URL
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import log
import pandas as pd
import ast

# pd.set_option('display.max_rows', None)

# pd.set_option('display.max_columns', None)

def main():
    print("Batch job started...")
    BASE_DIR = os.path.dirname(__file__)  # folder jahan __main__.py hai


    # 2️⃣ Fetch products from API and save CSV
    # fetch_products(products_cache_path)
    # Load from cache CSVs
    
    config = load_config(WP_API_URL)
    
    # products_df = pd.read_csv("products_cache.csv")
    # orders_df = pd.read_csv("orders_cache.csv")


    # orders_df = fetch_orders()
    # products_df = fetch_products()
    products_df = pd.read_csv(os.path.join(BASE_DIR, "products_cache.csv"))

    print("\n🛍️ Sample Products Loaded Successfully:")
    print(len(products_df))
    
    add_base.add_base()

 # Dummy orders generate karo
    df = generate_dummy_orders(
    products_csv=os.path.join(BASE_DIR, "add_base.csv"),
    output_csv=os.path.join(BASE_DIR, "structured_dummy_orders.csv")
    )

    print(df.head())


    # Create baskets
    baskets_df = create_baskets(df)
    print("\n🛍️ Sample Baskets Loaded Successfully:")
    # print(baskets_df)

    # Build similarity
    similarity_df = build_similarity(baskets_df,config)
    
    print("\n🛍️ Sample Similarity Scores Loaded Successfully:")
    print(similarity_df.head(50))

    # merged = similarity_df.merge(products_df, left_on="other_product", right_on="id", how="left", indicator=True)
    # print("DEBUG >> merge results")
    # print(merged[["product_id", "other_product", "_merge"]].head(20))

    # # #Apply filters
    filtered_df = apply_filters(similarity_df, products_df)
    print("\n🛍️ filtered Loaded Successfully:")
    print(len(filtered_df))

    
    
    
    
    recommendations = filtered_df.to_dict(orient="records")
    # print(recommendations)
    

    update_crosssell.save_recommendations(recommendations)

if __name__ == "__main__":
    main()
