from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.category import Category
from website.schemas.category import CategoryCreate, CategoryOut
from datetime import datetime

router = APIRouter(prefix="/categories", tags=["Categories"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a category
@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Get all categories
@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories
