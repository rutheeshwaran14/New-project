from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.user import User
from passlib.context import CryptContext
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def create_default_admin():
    db: Session = SessionLocal()

    admin = db.query(User).filter(
        User.email == settings.DEFAULT_ADMIN_EMAIL
    ).first()

    if not admin:
        admin = User(
            name="Admin",
            email=settings.DEFAULT_ADMIN_EMAIL,
            password_hash=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
            role="admin",
            is_verified=True
        )
        db.add(admin)
        db.commit()

    db.close()
