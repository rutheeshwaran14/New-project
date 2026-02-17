from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str
