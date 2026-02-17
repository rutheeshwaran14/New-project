from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.wishlist import Wishlist
from website.schemas import WishlistOut
from typing import List

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{product_id}")
def add_to_wishlist(product_id: int, db: Session = Depends(get_db)):
    wish = Wishlist(user_id=1, product_id=product_id)
    db.add(wish)
    db.commit()
    return {"message": "Added to wishlist"}


@router.get("/", response_model=List[WishlistOut])
def get_wishlist(db: Session = Depends(get_db)):
    return db.query(Wishlist).filter(Wishlist.user_id == 1).all()
