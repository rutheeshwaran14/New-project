from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from typing import List

from website.database import get_db
from website.models.wishlist import Wishlist
from website.models.user import User
from website.models.product import Product
from website.schemas import WishlistOut
from website.dependencies.auth import user_required

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.post("/{product_id}", response_model=WishlistOut, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Product already in wishlist")

    wish = Wishlist(user_id=current_user.id, product_id=product_id)
    db.add(wish)
    db.commit()
    db.refresh(wish)

    return wish


@router.get("/", response_model=List[WishlistOut])
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    wishlist_items = (
        db.query(Wishlist)
        .options(joinedload(Wishlist.product))   # 🔥 FIX: FORCE LOAD PRODUCT
        .filter(Wishlist.user_id == current_user.id)
        .all()
    )

    return wishlist_items


@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    wish = db.query(Wishlist).filter(
        Wishlist.user_id == current_user.id,
        Wishlist.product_id == product_id
    ).first()

    if not wish:
        return JSONResponse(
            status_code=404,
            content={"message": "Item not found in wishlist"}
        )

    db.delete(wish)
    db.commit()

    return {"message": "Removed from wishlist"}