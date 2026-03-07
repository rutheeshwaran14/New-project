from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from website.database import get_db
from website.models.order import Order
from website.dependencies.auth import get_current_user
from website.schemas.order import OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderOut])
def get_my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Get all orders of the current user, including items and product details.
    """
    orders = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return orders