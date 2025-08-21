import pandas as pd
import os

def load_orders_from_csv():
    """
    Load sample orders from CSV into a DataFrame.
    """
    csv_path = os.path.join(os.path.dirname(__file__), "../../sample_data/sample_orders.csv")
    df = pd.read_csv(csv_path)
    print("✅ Sample Orders Loaded Successfully:")
    print(df.head())
    return df
