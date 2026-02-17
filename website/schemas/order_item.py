from pydantic import BaseModel
from decimal import Decimal


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemOut(OrderItemBase):
    id: int
    price: Decimal

    class Config:
        from_attributes = True
