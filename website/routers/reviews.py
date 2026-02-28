# website/routers/reviews.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from website.database import get_db   
from website.models.review import Review
from website.models.user import User
from website.schemas import ReviewCreate, ReviewOut
from website.dependencies.auth import user_required

router = APIRouter(tags=["Reviews"])

# ➕ Create Review (Login Required)
@router.post("/products/{product_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    product_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    db_review = Review(
        **review.dict(),
        product_id=product_id,       # from URL
        user_id=current_user.id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 📥 Get Reviews for a Product (Public API)
@router.get("/products/{product_id}/reviews", response_model=List[ReviewOut])
def get_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Review).filter(
        Review.product_id == product_id
    ).all()