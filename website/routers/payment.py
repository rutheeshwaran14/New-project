# website/routers/payment.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from website.database import get_db
from website.models import Payment, Order, User
from website.auth import get_current_user

router = APIRouter(prefix="/payment", tags=["Payment"])

# ----------------- Initiate Payment -----------------
@router.post("/initiate/{order_id}")
def initiate_payment(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Simulate initiating a payment for a specific order.
    Generates a transaction ID.
    """

    # Find the order
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == user.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "PAID":
        raise HTTPException(status_code=400, detail="Order already paid")

    # Generate transaction ID
    transaction_id = str(uuid4())

    # ✅ FIX: ADD method="UPI"
    payment = Payment(
        order_id=order.id,
        user_id=user.id,
        transaction_id=transaction_id,
        amount=order.quantity * order.product.price,
        method="UPI",          # <<< THIS FIXES YOUR ERROR
        status="PENDING"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "transaction_id": transaction_id,
        "status": payment.status,
        "message": "Send this transaction_id to /callback/{transaction_id}?success=true"
    }

# ----------------- Payment Callback -----------------
@router.post("/callback/{transaction_id}")
def payment_callback(
    transaction_id: str,
    success: bool,
    db: Session = Depends(get_db)
):
    """
    Simulate payment confirmation from payment gateway.
    """

    payment = (
        db.query(Payment)
        .filter(Payment.transaction_id == transaction_id)
        .first()
    )

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if success:
        payment.status = "SUCCESS"

        order = db.query(Order).filter(Order.id == payment.order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        order.status = "PAID"

    else:
        payment.status = "FAILED"

    db.commit()

    return {
        "transaction_id": transaction_id,
        "payment_status": payment.status,
        "order_status": order.status if success else "UNPAID"
    }
