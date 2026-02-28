from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from website.database import get_db
from website.models.cart import Cart
from website.models.product import Product
from website.schemas import CartOut
from website.dependencies.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/{product_id}")
def add_to_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(404, "Product not found")

    cart_item = db.query(Cart).filter(
        Cart.user_id == user.id,
        Cart.product_id == product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=user.id,
            product_id=product_id,
            quantity=1
        )
        db.add(cart_item)

    db.commit()
    return {"message": "Added to cart"}


@router.get("/", response_model=List[CartOut])
def get_cart(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Cart).filter(Cart.user_id == user.id).all()


@router.put("/{product_id}")
def update_quantity(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart_item = db.query(Cart).filter(
        Cart.user_id == user.id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(404, "Item not found")

    if quantity < 1:
        raise HTTPException(400, "Quantity must be >= 1")

    cart_item.quantity = quantity
    db.commit()

    return {"message": "Quantity updated"}


@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart_item = db.query(Cart).filter(
        Cart.user_id == user.id,
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(404, "Item not found")

    db.delete(cart_item)
    db.commit()

    return {"message": "Removed from cart"}