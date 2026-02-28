from pydantic import BaseModel, EmailStr

# ---------------- Register ----------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# ---------------- Login (JSON) ----------------
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# ---------------- OTP ----------------
class OTPRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str