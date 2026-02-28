# website/routers/profile.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from website.database import get_db
from website.models.profile import Profile
from website.models.user import User
from website.schemas.profile import ProfileCreate, ProfileOut
from website.dependencies.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


# -------------------- GET PROFILE --------------------
@router.get("/", response_model=ProfileOut)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    # 🔥 Auto-create profile if not exists
    if not profile:
        profile = Profile(
            user_id=current_user.id,
            full_name="",
            phone="",
            address=""
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


# -------------------- CREATE / UPDATE PROFILE --------------------
@router.post("/", response_model=ProfileOut)
def create_or_update_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if profile:
        profile.full_name = profile_in.full_name
        profile.phone = profile_in.phone
        profile.address = profile_in.address
    else:
        profile = Profile(
            user_id=current_user.id,
            full_name=profile_in.full_name,
            phone=profile_in.phone,
            address=profile_in.address
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile