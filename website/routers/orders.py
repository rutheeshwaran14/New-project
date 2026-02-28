from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from website.database import get_db
from website.models.cart import Cart
from website.models.order import Order
from website.models.order_item import OrderItem
from website.dependencies.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


# ---------------- CHECKOUT ----------------
@router.post("/checkout")
def checkout(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0

    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {item.product.name}"
            )
        total += float(item.product.price) * item.quantity

    # Create order
    order = Order(
        user_id=user.id,
        total_amount=total,
        status="pending",
        payment_status="paid"
    )

    db.add(order)
    db.flush()   # ensures order.id exists

    # Create order items
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)

        # Reduce stock
        item.product.stock -= item.quantity

    # Clear cart
    db.query(Cart).filter(Cart.user_id == user.id).delete()

    db.commit()

    return {
        "message": "Order placed successfully",
        "order_id": order.id
    }


# ---------------- GET MY ORDERS ----------------
@router.get("/")
def get_my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )