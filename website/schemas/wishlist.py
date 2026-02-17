from pydantic import BaseModel
from datetime import datetime


class WishlistOut(BaseModel):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True
