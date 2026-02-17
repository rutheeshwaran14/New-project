from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from website.database import get_db
from website.models.user import User
from website.dependencies.auth import admin_required

router = APIRouter(prefix="/admin/users", tags=["Admin Users"])

# ---------------- Make a user a seller ----------------
@router.put("/make-seller/{user_id}", status_code=status.HTTP_200_OK)
def make_seller(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required)  # only admin can call
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.role == "seller":
        return {"message": "User is already a seller"}

    user.role = "seller"
    db.commit()
    return {
        "message": "User promoted to seller successfully",
        "user_id": user.id,
        "email": user.email,
        "new_role": user.role
    }

# ---------------- List all users (admin-only) ----------------
@router.get("/", response_model=list[dict])
def list_users(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "role": u.role, "is_verified": u.is_verified} for u in users]
