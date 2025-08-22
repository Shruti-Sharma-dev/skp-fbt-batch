from ingestion import orders, products
from processing import basketize, similarity
from publishing import update_crosssell
from ingestion.products import fetch_products
from ingestion.orders import fetch_orders
from processing.basketize import create_baskets
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import log
import pandas as pd


def main():
    print("Batch job started...")
    
    # # Fetch products
    # products_df = fetch_products()
    # print("\n🛍️ Sample Products Loaded Successfully:")
    # print(products_df.head())

    # Fetch orders
    orders_df = fetch_orders()
    print("\n🛍️ Sample Orders Loaded Successfully:")
    print(orders_df.head())


    baskets_df = create_baskets(orders_df)
    print("\n🛍️ Sample Baskets Loaded Successfully:")
    print(baskets_df.head(10))

if __name__ == "__main__":
    main()
