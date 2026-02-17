from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.review import Review
from website.schemas import ReviewCreate, ReviewOut
from typing import List

router = APIRouter(prefix="/reviews", tags=["Reviews"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict(), user_id=1)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/{product_id}", response_model=List[ReviewOut])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.product_id == product_id).all()
