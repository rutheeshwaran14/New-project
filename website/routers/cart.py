from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.cart import Cart
from website.models.product import Product
from website.schemas import CartBase, CartOut
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CartOut)
def add_to_cart(cart: CartBase, db: Session = Depends(get_db)):

    # 1. Check product exists
    product = db.query(Product).filter(Product.id == cart.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Add to cart
    db_cart = Cart(**cart.dict(), user_id=1)   # temp user
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


@router.get("/", response_model=List[CartOut])
def get_cart(db: Session = Depends(get_db)):
    return db.query(Cart).filter(Cart.user_id == 1).all()
