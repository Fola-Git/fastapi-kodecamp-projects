import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..models import Product, Order, User
from ..database import get_session
from ..security import get_current_user

ORDERS_JSON = Path(__file__).resolve().parents[1] / "orders.json"
router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("/add/")
def add_to_cart(product_id: int, quantity: int = 1, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    product = session.exec(select(Product).where(Product.id==product_id)).first()
    if not product or product.stock < quantity:
        raise HTTPException(400, "Invalid product or insufficient stock")
    # naive: reserve by decreasing stock
    product.stock -= quantity
    session.add(product); session.commit()
    return {"message":"Added to cart (reserved)", "product_id": product_id, "quantity": quantity}

@router.post("/checkout/")
def checkout(items: list[dict], session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    # items: [{product_id, quantity}]. Stock already reserved in add_to_cart in this demo.
    total = 0.0
    for item in items:
        p = session.get(Product, item["product_id"])
        if not p:
            raise HTTPException(400, f"Product {item['product_id']} not found")
        total += p.price * item["quantity"]
    order = Order(user_id=user.id, total_amount=total)
    session.add(order); session.commit(); session.refresh(order)
    # backup
    existing = []
    if ORDERS_JSON.exists():
        existing = json.loads(ORDERS_JSON.read_text())
    existing.append({"order_id": order.id, "user_id": user.id, "total_amount": total, "items": items})
    ORDERS_JSON.write_text(json.dumps(existing, indent=2))
    return {"order_id": order.id, "total": total}
