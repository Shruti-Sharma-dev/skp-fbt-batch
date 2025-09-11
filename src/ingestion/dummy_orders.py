import pandas as pd
from collections import defaultdict

# ---------- Step 1: Load products ----------
products_csv = "../products_cache.csv"
products = pd.read_csv(products_csv)

# Ensure categories and names are strings
products['categories'] = products['categories'].fillna('').astype(str)
products['name'] = products['name'].astype(str)

# ---------- Step 2: Define category mapping ----------
# Map all 42 categories into 6 main groups (example)
category_mapping = {
    'Fancy Pearl Set': 'Necklaces & Sets',
    'Necklace’s': 'Necklaces & Sets',
    'Plain Pink Pearl Set': 'Necklaces & Sets',
    'Fancy Pearls Sets': 'Necklaces & Sets',
    'Necklace Set': 'Necklaces & Sets',
    'Baroque Pearls': 'Necklaces & Sets',
    '92.5 Silver Jewellery Pearls Earrings': 'Earrings & Studs',
    'Pearl Earrings & Bangles': 'Earrings & Studs',
    'Bangles': 'Bracelets & Bangles',
    'Gift-product': 'Gift',
    'Uncategorized': 'Misc',
    'Luxury Pearl Set': 'Necklaces & Sets',
    'Long Pearl Set': 'Necklaces & Sets',
    'Chain’s': 'Chains',
    'Pearl Bracelet': 'Bracelets & Bangles',
    'Choker Set': 'Necklaces & Sets',
    'Single Line Pearl Set': 'Necklaces & Sets',
    'Plain Pearl Sets': 'Necklaces & Sets',
    'Precious Stones': 'Gemstones',
    'Emerald': 'Gemstones',
    'Pearl Pendent Set': 'Necklaces & Sets',
    'Simple Pearl Necklace Set': 'Necklaces & Sets',
    'Pearl Bangle': 'Bracelets & Bangles',
    '92.5 Silver Pearl Jewellery': 'Jewellery',
    'Exclusive Pearls Set': 'Necklaces & Sets',
    'Plain Black Pearl Set': 'Necklaces & Sets',
    'Double Line Pearl Set': 'Necklaces & Sets',
    'Button Pearl Set': 'Necklaces & Sets',
    'Pearls Earrings': 'Earrings & Studs',
    'Plain Grey Pearl Set': 'Necklaces & Sets',
    'Ruby': 'Gemstones',
    'Three Line Pearl Necklace set': 'Necklaces & Sets',
    'Rani Haar': 'Necklaces & Sets',
    'Precious Stones Studs': 'Earrings & Studs',
    'Broch Set': 'Brooches',
    'Pearl Necklace Sets': 'Necklaces & Sets',
    'Plain White Pearl Set': 'Necklaces & Sets',
    'Designer sets': 'Necklaces & Sets',
    '92.5 Silver Jewellery': 'Jewellery',
    'Pearl Studs Earrings': 'Earrings & Studs',
    'Pearl Hanging': 'Earrings & Studs',
    'Hyderabadi Pearls': 'Necklaces & Sets'
}

# ---------- Step 3: Define complementary groups ----------
complementary = {
    'Necklaces & Sets': ['Earrings & Studs', 'Bracelets & Bangles'],
    'Earrings & Studs': ['Necklaces & Sets', 'Bracelets & Bangles'],
    'Bracelets & Bangles': ['Necklaces & Sets', 'Earrings & Studs']
}

# ---------- Step 4: Extract material ----------
def get_material(product_name):
    """
    Simple material extraction based on keywords in product name.
    """
    name = product_name.lower()
    materials = ['pearl', 'ruby', 'emerald', 'gold', 'silver']
    for mat in materials:
        if mat in name:
            return mat.capitalize()
    return 'Misc'

products['material'] = products['name'].apply(get_material)

# ---------- Step 5: Group products by category ----------
products['main_group'] = products['categories'].map(category_mapping).fillna('Misc')
products_by_group = defaultdict(list)
for idx, row in products.iterrows():
    products_by_group[row['main_group']].append({
        'id': row['id'],
        'name': row['name'],
        'material': row['material']
    })

# ---------- Step 6: Generate recommendations ----------
recommendations = defaultdict(list)

for idx, row in products.iterrows():
    main_product_id = row['id']
    main_group = row['main_group']
    main_material = row['material']
    
    recs = []
    for comp_group in complementary.get(main_group, []):
        for p in products_by_group[comp_group]:
            if p['material'] == main_material:
                recs.append(p['id'])
    
    # Remove duplicates & main product itself
    recs = list(set(recs) - {main_product_id})
    recommendations[main_product_id] = recs

# ---------- Step 7: Convert to DataFrame ----------
rec_df = pd.DataFrame([
    {'product_id': pid, 'recommended_ids': recs} 
    for pid, recs in recommendations.items()
])

# ---------- Step 8: Save to CSV ----------
output_csv = "../output/recommendations.csv"
rec_df.to_csv(output_csv, index=False)

print(f"Recommendations generated for {len(rec_df)} products!")
print(rec_df.head())
