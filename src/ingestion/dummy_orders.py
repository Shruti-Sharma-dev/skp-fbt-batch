import pandas as pd
import random

def generate_structured_orders(products_df: pd.DataFrame, num_orders: int = 50) -> pd.DataFrame:
    """
    Generate dummy orders ensuring products are grouped by category.
    
    Args:
        products_df: DataFrame with columns ["id", "category"]
        num_orders: how many dummy orders to generate
    
    Returns:
        DataFrame of dummy orders with columns ["order_id", "product_id"]
    """


    # Group products by category
    category_groups = (
        products_df.groupby("categories")["id"]
        .apply(list)
        .to_dict()
    )

    categories = list(category_groups.keys())

    orders = []

    for order_id in range(1, num_orders + 1):
        # Pick a primary category
        primary_category = random.choice(categories)
        primary_products = category_groups[primary_category]

        # Select 2–3 products from this category
        basket_products = random.sample(
            primary_products, min(len(primary_products), random.randint(2, 3))
        )

        # Pick a complementary category (different from primary)
        other_categories = [c for c in categories if c != primary_category]
        if other_categories:  # avoid error if only one category
            secondary_category = random.choice(other_categories)
            secondary_products = category_groups[secondary_category]

            # Add 2–3 products from secondary category
            basket_products += random.sample(
                secondary_products, min(len(secondary_products), random.randint(2, 3))
            )

        # Ensure 4–6 unique items per basket
        basket_products = list(set(basket_products))[: random.randint(4, 6)]

        # Add to orders
        for pid in basket_products:
            orders.append({"order_id": order_id, "product_id": pid})

    dummy_orders_df = pd.DataFrame(orders)
    dummy_orders_df.to_csv("dummy_orders.csv", index=False)

    return dummy_orders_df


# Example usage
if __name__ == "__main__":
    # Load your cached products file (must have id, category columns)
    products_df = pd.read_csv("products.csv")
    dummy_orders_df = generate_dummy_orders(products_df, num_orders=25)
    print(dummy_orders_df.head())
