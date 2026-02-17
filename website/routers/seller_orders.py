from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from website.database import get_db
from website.models.order import Order
from website.dependencies.auth import seller_required

router = APIRouter(prefix="/seller/orders", tags=["Seller Orders"])


@router.get("/")
def seller_orders(
    db: Session = Depends(get_db),
    seller = Depends(seller_required)
):
    return (
        db.query(Order)
        .join(Order.items)
        .filter(Order.seller_id == seller.id)
        .all()
    )
