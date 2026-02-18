from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.payment import Payment
from website.schemas import PaymentCreate, PaymentOut
from website.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentOut)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
