from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.cart import Cart
from website.models.order import Order
from website.models.order_item import OrderItem
from website.models.product import Product
from website.dependencies.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def place_order(db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()

    if not cart_items:
        raise HTTPException(400, "Cart is empty")

    total = 0

    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(400, f"Insufficient stock for {item.product.name}")
        total += item.product.price * item.quantity

    order = Order(user_id=user.id, total_amount=total, status="confirmed")
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        ))

        # 🔻 Reduce stock
        item.product.stock -= item.quantity

    db.query(Cart).filter(Cart.user_id == user.id).delete()
    db.commit()

    return {"message": "Order placed successfully", "order_id": order.id}

from datetime import datetime

@router.put("/{order_id}/cancel")
def cancel_order(order_id: int,
                 db: Session = Depends(get_db),
                 user=Depends(get_current_user)):

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user.id,
        Order.is_deleted == False
    ).first()

    if not order:
        raise HTTPException(404, "Order not found")

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock += item.quantity  # 🔼 Restore stock

    order.status = "cancelled"
    order.is_deleted = True
    order.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Order cancelled & stock restored"}
