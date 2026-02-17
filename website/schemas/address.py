from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    address_line1: str
    address_line2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str = "India"


class AddressCreate(AddressBase):
    pass


class AddressOut(AddressBase):
    id: int
    is_default: bool

    class Config:
        from_attributes = True
