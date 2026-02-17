from pydantic import BaseModel


class CartBase(BaseModel):
    product_id: int
    quantity: int


class CartOut(CartBase):
    id: int

    class Config:
        from_attributes = True
