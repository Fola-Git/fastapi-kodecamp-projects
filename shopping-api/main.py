from fastapi import FastAPI, Query
from cart import add_to_cart, checkout_cart

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 500},
    {"id": 2, "name": "Headphones", "price": 150},
    {"id": 3, "name": "Keyboard", "price": 100},
    {"id": 4, "name": "Monitor", "price": 300}
]

@app.get("/products/")
def get_products():
    return products

@app.post("/cart/add")
def add_item_to_cart(product_id: int = Query(...), qty: int = Query(...)):
    result = add_to_cart(product_id, qty, products)
    if "error" in result:
        return {"detail": result["error"]}
    return {"message": "Item added to cart", "cart": result}

@app.get("/cart/checkout")
def checkout():
    return checkout_cart()
