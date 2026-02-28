# schemas/profile.py
from pydantic import BaseModel

class ProfileBase(BaseModel):
    full_name: str
    phone: str | None = None
    address: str | None = None

class ProfileCreate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True