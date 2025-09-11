import pandas as pd

df = pd.read_csv("../src/products_cache.csv")

# Fill NaNs

df['categories'] = df['categories'].fillna('').astype(str)

all_categories = set()

for cats in df['categories']:
    # Split by comma, strip spaces, ignore empty
    split_cats = [c.strip() for c in cats.split(',') if c.strip() != '']
    all_categories.update(split_cats)

print(len(all_categories))
print(all_categories)

products_csv_path = "../src/products_cache.csv"  