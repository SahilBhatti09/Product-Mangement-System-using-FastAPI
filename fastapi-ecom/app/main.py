from fastapi import FastAPI, Query, HTTPException, Path as FPath, Depends
from service.products import load_products, get_all_product, add_product, remove_product, change_product
from schema.product import Product, ProductUpdate
from uuid import uuid4, UUID
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

load_dotenv()
app = FastAPI()
# GET - READ, POST - CREATE, PUT - UPDATE, DELETE - DELETE

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------- ROOT PAGE ---------------------------------
@app.get("/", response_model=dict)
def get_root():
    return{"message": "THIS IS MY ROOT PAGE"}

# --------------------------------- READ ALL PRODUCTS ---------------------------------
@app.get("/products")     # filter by names
def list_all_products(
    dep=Depends(load_products),
    name: str = Query(
        default=None,
        min_length=1,
        max_length=100, 
        description="Search by product name (case insensitive)",
    ),
    sort_by_price: bool = Query(
        default=False,
        description="Sort products by price",
    ),
    order:str=Query(
        default="asc",
        description="Sort order when sort_by_price=true (asc or desc)"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Limit the number of products to return",
    ),
    offset: int = Query(
        default=0,
        ge=1,   
        description="Pagination offset",
    ),
):
    
    #products = get_all_product()
    products = dep
    total = len(products)

    # 🔍 Filter by name:
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name","").lower()]

        if not products:
            raise HTTPException(
                status_code=404, 
                detail=f"No products found matched name: {name}",)   

    # 🔍 Sort by price:
        if sort_by_price:
            reverse = order == "desc"
            products.sort(key=lambda p: p.get("price",0), reverse=reverse)

        total = len(products)
        
        # ✂️ Limit (ALWAYS applied)    
        # # products = products[0:limit]
        products = products[offset:offset+limit]
    return {"total": total, "limit": limit, "items": products}

# --------------------------------- READ ---------------------------------
@app.get("/products/{product_id}", response_model=dict)
def get_product(
    product_id: str = FPath(
        ..., min_length=36, max_length=100, description="The ID of the product", examples=[{"0005a4ea-ce3f-4dd7-bee0-f4ccc70fea6a"}])):

    products = get_all_product()
    for p in products:
         if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

# --------------------------------- CREATE ---------------------------------
@app.post("/products", status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.now(timezone.utc).isoformat()
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return product.model_dump(mode="json")

# --------------------------------- DELETE ---------------------------------
@app.delete("/products/{product_id}")
def delete_product(
    product_id: UUID = FPath(
        ...,
        description="Product UUID",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
):
    try:
        rem = remove_product(str(product_id))
        return rem
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------------------- UPDATE ---------------------------------
@app.put("/products/{product_id}")
def update_product(
    product_id: UUID = FPath( ..., description="Product UUID"), 
    payload: ProductUpdate = ...,
):
    try:
        update_product = change_product(
            str(product_id),payload.model_dump(mode="json",exclude_unset=True)
        )
        return update_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 
