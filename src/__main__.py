from ingestion import orders, products
from processing import basketize, similarity
from publishing import update_crosssell
from utils.helpers import log

def main():
    log("Batch job started (Week 1 skeleton)")

    # Load sample data
    order_data = orders.load_sample_orders("../sample_data/sample_orders.json")
    product_data = products.load_sample_products("../sample_data/sample_products.csv")

    log(f"Loaded {len(order_data)} orders and {len(product_data)} products")

    # Processing
    baskets = basketize.create_baskets(order_data)
    recommendations = similarity.compute_recommendations(baskets)

    # Publishing
    update_crosssell.push_dummy(recommendations)

    log("Batch job completed (Week 1 skeleton)")


if __name__ == "__main__":
    main()
