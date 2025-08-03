import json
import math

CART_FILE = "cart.json"

def load_cart():
    try:
        with open(CART_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_cart(cart):
    with open(CART_FILE, "w") as f:
        json.dump(cart, f, indent=4)

def add_to_cart(product_id: int, qty: int, products: list):
    cart = load_cart()

    # Find product by ID
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found."}

    item_name = product["name"]
    price = product["price"]
    total_price = round(price * qty, 2)

    if item_name in cart:
        cart[item_name]["quantity"] += qty
        cart[item_name]["total"] = round(cart[item_name]["quantity"] * price, 2)
    else:
        cart[item_name] = {
            "price": price,
            "quantity": qty,
            "total": total_price
        }

    save_cart(cart)
    return cart

def checkout_cart():
    cart = load_cart()
    total_amount = sum(item["total"] for item in cart.values())
    total_amount = math.ceil(total_amount)  # or round(total_amount, 2)
    return {"cart": cart, "total": total_amount}
