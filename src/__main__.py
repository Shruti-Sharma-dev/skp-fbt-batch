from ingestion import orders, products
from processing import basketize, similarity
from publishing import update_crosssell
from ingestion.products import fetch_products
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import log
import pandas as pd


def main():
    print("Batch job started...")
    
    # Fetch products
    products_df = fetch_products()
    print("\n🛍️ Sample Products Loaded Successfully:")
    print(products_df.head())



if __name__ == "__main__":
    main()
