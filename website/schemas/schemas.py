from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

# ----------------- User -----------------
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

from pydantic import BaseModel, EmailStr
from typing import Annotated
from pydantic import Field

class UserCreate(BaseModel):
    name: str  # changed from username
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]

class UserOut(BaseModel):
    id: int
    name: str  # changed from username
    email: EmailStr

    model_config = {
        "from_attributes": True  # allows SQLAlchemy objects to work with Pydantic
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
from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    model_config = {"from_attributes": True}


class CancelOrder(BaseModel):
    reason: str
