from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

# ----------------- User -----------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]  # bcrypt truncation handled later

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

# ----------------- Product -----------------
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int

class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int

    model_config = {
        "from_attributes": True
    }

# ----------------- Order -----------------
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True
    }
