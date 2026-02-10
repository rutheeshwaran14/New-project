from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
class CartAdd(BaseModel):
    product_id: int
    quantity: int

class CartOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = {"from_attributes": True}
