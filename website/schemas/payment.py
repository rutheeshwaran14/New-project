from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class PaymentCreate(BaseModel):
    order_id: int
    amount: Decimal
    method: str


class PaymentOut(BaseModel):
    id: int
    amount: Decimal
    method: str
    status: str
    transaction_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True
