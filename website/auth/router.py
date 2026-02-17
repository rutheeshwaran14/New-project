from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from website.database import get_db
from website.models.user import User
from website.auth.schemas import UserRegister, OTPVerify, LoginSchema
from website.auth.utils import generate_otp, otp_expiry_time
from website.auth.email import send_otp_email
from website.auth.jwt import create_access_token
from email.message import EmailMessage
import smtplib
from config import SMTP_EMAIL, SMTP_PASSWORD

from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- REGISTER ----------------
@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd_context.hash(data.password)
    otp = generate_otp()

    new_user = User(
        name=data.name,
        email=data.email,
        password=hashed,
        role="user",
        is_verified=False,
        otp_code=otp,
        otp_expiry=otp_expiry_time()
    )

    db.add(new_user)
    db.commit()

    send_otp_email(data.email, otp)

    return {"message": "OTP sent to your email. Please verify."}


# ---------------- VERIFY OTP ----------------
@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Already verified"}

    if user.otp_code != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.utcnow() > user.otp_expiry:
        raise HTTPException(status_code=400, detail="OTP expired")

    user.is_verified = True
    user.otp_code = None
    user.otp_expiry = None

    db.commit()

    return {"message": "Email verified successfully"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before login"
        )

    token = create_access_token({"user_id": user.id, "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify Your Account"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
Your OTP is: {otp}

Valid for 10 minutes.
""")

