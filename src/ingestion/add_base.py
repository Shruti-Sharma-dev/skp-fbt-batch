
import pandas as pd
import os

import numpy as np

import sys, os

def add_base():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print(BASE_DIR)
    products_cache_path = os.path.join(BASE_DIR, "products_cache.csv")

    add_csv_path = os.path.join(BASE_DIR, "add_base.csv")
    print(add_csv_path)
    df = pd.read_csv(products_cache_path)

    filtered = df[df['categories'].notna() & df['name'].notna()]

    print(filtered.head(10))

    conditions=[
        filtered['categories'].str.contains('necklace|set|choker|haar|chain', case=False, na=False) | filtered['name'].str.contains('necklace|set|choker|haar|chain', case=False, na=False) ,
        filtered['categories'].str.contains('studs|tops', case=False, na=False) | filtered['name'].str.contains('studs|tops', case=False, na=False),
        filtered['categories'].str.contains('earrings|hanging|chand baali|jhumka', case=False, na=False) | filtered['name'].str.contains('earrings|hanging|chand baali|jhumka', case=False, na=False),
        filtered['categories'].str.contains('bracelet', case=False, na=False) | filtered['name'].str.contains('bracelet', case=False, na=False),
        filtered['categories'].str.contains('ring', case=False, na=False) | filtered['name'].str.contains('necklace|set|choker|haar|chain', case=False, na=False),
        filtered['categories'].str.contains('bangle', case=False, na=False) | filtered['name'].str.contains('bangle', case=False, na=False),
        filtered['categories'].str.contains('stones|ruby|emerald', case=False, na=False) | filtered['name'].str.contains('stones|ruby|emerald', case=False, na=False),
    
    ]

    choices = ['necklace','studs','earrings', 'bracelet', 'ring', 'bangle', 'stone']



    filtered["base_category"] = np.select(conditions, choices, default='others')




    conditions_material = [

        ((filtered['name'].str.contains('emerald', case=False, na=False)) | (filtered['categories'].str.contains('emerald', case=False, na=False))),
        ((filtered['name'].str.contains('ruby', case=False, na=False)) | (filtered['categories'].str.contains('ruby', case=False, na=False))),
        ((filtered['name'].str.contains('oyster', case=False, na=False)) | (filtered['categories'].str.contains('oyster', case=False, na=False))),
        ((filtered['name'].str.contains('sapphire', case=False, na=False)) | (filtered['categories'].str.contains('sapphire', case=False, na=False))),
        ((filtered['name'].str.contains('gold', case=False, na=False)) | (filtered['categories'].str.contains('gold', case=False, na=False))),
        ((filtered['name'].str.contains('silver', case=False, na=False)) | (filtered['categories'].str.contains('silver', case=False, na=False))),
        ((filtered['name'].str.contains('coral', case=False, na=False)) | (filtered['categories'].str.contains('coral', case=False, na=False))),
        ((filtered['name'].str.contains('pearl', case=False, na=False)) | (filtered['categories'].str.contains('pearl', case=False, na=False))),
    ]


    choices_material = [ 'emerald', 'ruby', 'oyster' , 'sapphire', 'gold','silver' , 'coral' , 'pearl']



    filtered["material"] = np.select(conditions_material, choices_material, default='others')



    conditions_color = [
        (filtered['name'].str.contains('black', case=False, na=False)) | (filtered['categories'].str.contains('black', case=False, na=False)),
        (filtered['name'].str.contains('pink', case=False, na=False))  | (filtered['categories'].str.contains('pink', case=False, na=False)),
        (filtered['name'].str.contains('gold', case=False, na=False))  | (filtered['categories'].str.contains('gold', case=False, na=False)),
        (filtered['name'].str.contains('gray', case=False, na=False))  | (filtered['categories'].str.contains('gray', case=False, na=False)),
        (filtered['name'].str.contains('brown', case=False, na=False)) | (filtered['categories'].str.contains('brown', case=False, na=False)),
        (filtered['name'].str.contains('blue', case=False, na=False))  | (filtered['categories'].str.contains('blue', case=False, na=False)),
        (filtered['name'].str.contains('purple', case=False, na=False)) | (filtered['categories'].str.contains('purple', case=False, na=False)),
        (filtered['name'].str.contains('green', case=False, na=False))  | (filtered['categories'].str.contains('green', case=False, na=False))
    ]



    choices_colors = ['black', 'pink' , 'gold', 'gray', 'brown', 'blue', 'purple', 'green']




    filtered["color"] = np.select(conditions_color, choices_colors, default='other')
    filtered.to_csv(add_csv_path, index=False)

    return 