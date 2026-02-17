from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderCreate(BaseModel):
    user_id: int
    total_amount: float
    status: Optional[str] = "pending"
    payment_status: Optional[str] = "pending"


class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime

    class Config:
        from_attributes = True
