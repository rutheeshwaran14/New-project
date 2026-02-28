from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    price: float
    image: str | None

    class Config:
        orm_mode = True

class WishlistOut(BaseModel):
    id: int
    product: ProductBase

    class Config:
        orm_mode = True