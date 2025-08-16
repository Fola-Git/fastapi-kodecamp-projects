from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json, os

from auth import User, get_current_user, require_role

app = FastAPI(title="Shopping Cart API")

PRODUCTS_FILE = "products.json"
CART_FILE = "cart.json"

class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)

class AddProductRequest(BaseModel):
    name: str
    price: float
    stock: int = 0

class CartAddRequest(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

def read_json(path: str, default):
    if not os.path.exists(path):
        try:
            with open(path, "w") as f:
                json.dump(default, f, indent=2)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Init {path} error: {e}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Read {path} error: {e}")

def write_json(path: str, payload):
    try:
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Write {path} error: {e}")

@app.post("/admin/add_product/")
def add_product(req: AddProductRequest, admin: User = Depends(require_role("admin"))):
    data = read_json(PRODUCTS_FILE, [])
    next_id = (max([p["id"] for p in data]) + 1) if data else 1
    product = Product(id=next_id, name=req.name, price=req.price, stock=req.stock)
    data.append(product.model_dump())
    write_json(PRODUCTS_FILE, data)
    return {"message": "Product added", "product": product}

@app.get("/products/")
def list_products():
    data = read_json(PRODUCTS_FILE, [])
    return {"products": data}

@app.post("/cart/add/")
def add_to_cart(req: CartAddRequest, user: User = Depends(get_current_user)):
    products = read_json(PRODUCTS_FILE, [])
    prod = next((p for p in products if p["id"] == req.product_id), None)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    if req.quantity > prod.get("stock", 0):
        raise HTTPException(status_code=400, detail="Insufficient stock")
    # decrement stock
    prod["stock"] -= req.quantity
    write_json(PRODUCTS_FILE, products)

    cart = read_json(CART_FILE, {})
    user_cart = cart.get(user.username, [])
    user_cart.append({"product_id": req.product_id, "quantity": req.quantity})
    cart[user.username] = user_cart
    write_json(CART_FILE, cart)
    return {"message": "Added to cart", "cart": user_cart} 