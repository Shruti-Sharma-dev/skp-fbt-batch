import pandas as pd
import random

# Your product IDs (example)


def generate_dummy_orders(orders_df: pd.DataFrame) -> pd.DataFrame:
    product_ids = orders_df['id'].unique().tolist()  # replace with your full list
    num_orders = 50  # how many dummy orders you want

    orders = []

    for order_id in range(1, num_orders + 1):
    # randomly pick 5-6 products per basket
        basket_size = random.randint(5, 6)
        basket_products = random.sample(product_ids, min(basket_size, len(product_ids)))
    
        for product in basket_products:
            orders.append({"order_id": order_id, "product_id": product})

# Create DataFrame
    dummy_orders_df = pd.DataFrame(orders)

# Save to CSV
    dummy_orders_df.to_csv("dummy_orders.csv", index=False)

    return dummy_orders_df
