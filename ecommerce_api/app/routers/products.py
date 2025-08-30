from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..models import Product
from ..database import get_session
from ..security import get_current_admin

router = APIRouter(tags=["products"])

@router.post("/admin/products/")
def create_product(name: str, price: float, stock: int, admin = Depends(get_current_admin), session: Session = Depends(get_session)):
    p = Product(name=name, price=price, stock=stock)
    session.add(p); session.commit(); session.refresh(p)
    return p

@router.get("/products/")
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()
