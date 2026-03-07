from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    image: Optional[str]

    class Config:
        orm_mode = True


class OrderItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int
    price: float

    class Config:
        orm_mode = True


class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        orm_mode = True