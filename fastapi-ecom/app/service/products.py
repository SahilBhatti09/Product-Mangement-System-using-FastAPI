from schema.product import Product
from typing import List, Dict
import json
import json
from pathlib import Path
from typing import List, Dict
from fastapi import HTTPException

DATA_FILE = Path(__file__).parent.parent/"data"/"products.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_product()-> List[Dict]:
    return load_products()

# --------------------------------- CREATE ---------------------------------
def save_product(products: List[Dict])-> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def add_product(product: Dict)-> Dict:
    products = get_all_product()
    
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("Product with this SKU already exists")
    
    products.append(product)
    save_product(products)
    return product

# --------------------------------- DELETE ---------------------------------
def remove_product(id:str)-> dict:
    products = get_all_product()
    for index, p in enumerate(products): # Enumerate - index and values both
        if p['id'] == str(id):
            deleted = products.pop(index)
            save_product(products)
            return {"message": "Deleted product: "+deleted['name']}
    raise ValueError("Product not found")

# --------------------------------- UPDATE ---------------------------------
def change_product(product_id:str, update_data: Dict):
    products = get_all_product()
    for index, product in enumerate(products):
        if product['id'] == product_id:

            for key, value in update_data.items(): # convert the update_data to a dictionary
                if value is None:
                    continue 

                if isinstance(value, dict) and isinstance(product.get(key), dict):
                    product[key].update(value)
                else:
                    product[key] = value

            products[index] = product
            save_product(products)
            return product
            
    raise ValueError("Product not found")