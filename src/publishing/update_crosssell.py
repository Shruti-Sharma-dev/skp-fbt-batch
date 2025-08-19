# update_crosssell.py
def push_dummy(recommendations):
    """
    Placeholder: simulate publishing recommendations
    For now, just print top 2-3 recommendations per product
    """
    print("\nPublishing Dummy Recommendations:")
    for prod_id, recs in list(recommendations.items())[:5]:  # top 5 products
        print(f"Product {prod_id}: recommended -> {recs[:3]}")
