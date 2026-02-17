from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime

from website.database import SessionLocal
from website.models.user import User
from website.models.user_otp import UserOTP
from website.dependencies.auth import get_current_user
from website.utils.jwt import create_access_token
from website.utils.otp import generate_otp, otp_expiry
from website.utils.email import send_otp_email
from website.schemas.auth import UserCreate, OTPRequest, OTPVerify

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- Database session ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Password utilities ----------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ---------------- Register endpoint ----------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password),
        is_verified=False,
        role="user"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully"}

# ---------------- Login endpoint (Swagger-ready) ----------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not db_user.password_hash:
        raise HTTPException(status_code=401, detail="Password login not available")

    if not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": str(db_user.id),
        "role": db_user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ---------------- Send OTP ----------------
@router.post("/send-otp")
def send_otp(data: OTPRequest, db: Session = Depends(get_db)):
    otp = generate_otp()

    otp_entry = UserOTP(
        email=data.email,
        otp_code=otp,
        expires_at=otp_expiry()
    )

    db.add(otp_entry)
    db.commit()

    send_otp_email(data.email, otp)

    return {"message": "OTP sent successfully"}

# ---------------- Verify OTP ----------------
@router.post("/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    otp_entry = db.query(UserOTP).filter(
        UserOTP.email == data.email,
        UserOTP.otp_code == data.otp,
        UserOTP.is_used == False
    ).order_by(UserOTP.created_at.desc()).first()

    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_entry.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    otp_entry.is_used = True

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        user = User(
            email=data.email,
            is_verified=True,
            role="user"
        )
        db.add(user)

    user.is_verified = True
    db.commit()
    db.refresh(user)

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "message": "OTP verified successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }
