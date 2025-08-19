import pandas as pd
import os

# Correct path: go one level up from current file
csv_path = os.path.join(os.path.dirname(__file__), "../../sample_data/sample_products.csv")

# Load CSV
products_df = pd.read_csv(csv_path)

# Preview data
print("Sample Products Loaded Successfully:")
print(products_df.head())
