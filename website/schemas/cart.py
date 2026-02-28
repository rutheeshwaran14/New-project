from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class CartProductOut(BaseModel):
    id: int
    name: str
    price: Decimal
    image: Optional[str]

    class Config:
        from_attributes = True


class CartBase(BaseModel):
    product_id: int
    quantity: int


class CartOut(BaseModel):
    id: int
    quantity: int
    product: CartProductOut

    class Config:
        from_attributes = True