from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from website.database import get_db   
from website.models.review import Review
from website.models.user import User
from website.schemas import ReviewCreate, ReviewOut
from website.dependencies.auth import user_required

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# ➕ Create Review (Login Required)
@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    db_review = Review(
        **review.dict(),
        user_id=current_user.id   # 👈 dynamic user id
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


# 📥 Get Reviews for a Product (Public API)
@router.get("/{product_id}", response_model=List[ReviewOut])
def get_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Review).filter(
        Review.product_id == product_id
    ).all()
