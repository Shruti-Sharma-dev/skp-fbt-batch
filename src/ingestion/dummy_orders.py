import pandas as pd
import random
from collections import defaultdict

def generate_dummy_orders(products_csv, output_orders_csv, num_orders=5000):
    products = pd.read_csv(products_csv)
    product_ids = products['id'].tolist()

    orders = []
    used_products = set()

    for order_id in range(1, num_orders+1):
        # Random basket size: 3–8
        basket_size = random.randint(3, 8)

        # Ensure coverage: force-inject unused products in first 90% orders
        if len(used_products) < int(0.9 * len(product_ids)):
            prod = random.choice([p for p in product_ids if p not in used_products])
            basket = {prod}
            used_products.add(prod)
        else:
            basket = set()

        # Fill remaining basket with random products
        while len(basket) < basket_size:
            basket.add(random.choice(product_ids))

        # Save basket rows
        for pid in basket:
            orders.append([order_id, pid, 1])  # quantity = 1

    df_orders = pd.DataFrame(orders, columns=["order_id", "product_id", "quantity"])
    return df_orders

