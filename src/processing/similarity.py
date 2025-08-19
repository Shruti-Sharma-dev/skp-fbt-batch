# similarity.py
def compute_recommendations(baskets):
    """
    Simple placeholder: create item-to-item co-occurrence recommendations
    Returns dict {product_id: [rec_product_ids]}
    """
    from collections import defaultdict
    recommendations = defaultdict(list)
    
    for basket in baskets:
        for i, prod in enumerate(basket):
            recs = basket[:i] + basket[i+1:]  # all other items in same basket
            recommendations[prod].extend(recs)
    
    # Remove duplicates and limit top 3 recommendations
    for prod in recommendations:
        recommendations[prod] = list(set(recommendations[prod]))[:3]
    
    return recommendations
