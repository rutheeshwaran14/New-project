from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: Decimal
    stock: int
    category_id: int
    image: Optional[str] = None   # 🔥 ADD THIS


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    stock: Optional[int]
    category_id: Optional[int]
    image: Optional[str] = None   # 🔥 ADD THIS


class ProductOut(ProductBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True