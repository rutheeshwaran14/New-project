from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.user import User
from config import settings

# -------------------- OAuth2 Bearer token --------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# -------------------- Database session --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Get current user --------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# -------------------- Admin required --------------------
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# -------------------- Seller required (admin can bypass) --------------------
def seller_required(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Seller access required")
    return current_user

# -------------------- User required (admin can bypass) --------------------
def user_required(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("user", "admin"):
        raise HTTPException(status_code=403, detail="User access required")
    return current_user
