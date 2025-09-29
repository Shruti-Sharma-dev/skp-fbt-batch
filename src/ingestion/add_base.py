
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

products_cache_path = os.path.join(BASE_DIR, "products_cache.csv")

add_csv_path = os.path.join(BASE_DIR, "add_base.csv")

df = pd.read_csv(products_cache_path)

filtered = df[df['categories'].notna() & df['name'].notna()]

print(filtered.head(10))

conditions=[
    filtered['categories | name'].str.contains('necklace|set|choker|haar', case=False, na=False),
    filtered['categories'].str.contains('earrings|studs|hanging', case=False, na=False),
    filtered['categories'].str.contains('bracelet', case=False, na=False),
    filtered['categories'].str.contains('ring', case=False, na=False),
    filtered['categories'].str.contains('bangle', case=False, na=False),
    filtered['categories'].str.contains('stones|ruby|emerald', case=False, na=False),
  
]
    
choices = ['necklace', 'earrings', 'bracelet', 'ring', 'bangle', 'stone']



filtered["base_categgory"] = np.select(conditions, choices, default='others')




conditions_material = [
    filtered['categories | name'].str.contains('pearl', case=False, na=False),
    
]

choices_material = ['pearl']

filtered["material"] = np.select(conditions_material, choices_material, default='others')

filtered.to_csv("add_base.csv", index=False)