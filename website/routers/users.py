from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.user import User
from website.schemas import UserOut
from typing import List
from website.dependencies.auth import admin_required
from website.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    return db.query(User).all()