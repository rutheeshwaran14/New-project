from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from website.database import get_db
from website.models import Product, Order
from website.models.cart import Cart
from website.schemas.orders import CartAdd, CartOut
from website.auth import get_current_user

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

router = APIRouter(prefix="/cart", tags=["Cart"])


# ---------------- Add to cart ----------------
@router.post("/add", response_model=CartOut)
def add_to_cart(
    item: CartAdd,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = db.query(Cart).filter(
        Cart.user_id == user.id,
        Cart.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = Cart(
            user_id=user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    FastAPICache.clear()
    return cart_item


# ---------------- Update cart ----------------
@router.put("/{cart_id}")
def update_cart(
    cart_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity
    db.commit()
    FastAPICache.clear()
    return {"message": "Quantity updated"}


# ---------------- Remove item ----------------
@router.delete("/{cart_id}")
def remove_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    FastAPICache.clear()
    return {"message": "Item removed from cart"}


# ---------------- Checkout ----------------
@router.post("/checkout")
def checkout(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}"
            )

        product.stock -= item.quantity

        order = Order(
            user_id=user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(order)
        db.delete(item)

    db.commit()
    FastAPICache.clear()
    return {"message": "Order placed successfully"}


# ---------------- View cart ----------------
@router.get("/", response_model=list[CartOut])
@cache(expire=30)
def view_cart(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Cart).filter(Cart.user_id == user.id).all()
