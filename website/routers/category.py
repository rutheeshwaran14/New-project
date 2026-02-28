from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from website.database import get_db
from website.models.category import Category
from website.models.product import Product
from website.schemas.category import CategoryCreate, CategoryOut
from website.schemas.product import ProductOut

router = APIRouter(prefix="/categories", tags=["Categories"])

# Create a category
@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Get all categories
@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories

# Get products by category
@router.get("/{category_id}/products", response_model=List[ProductOut])
def get_category_products(category_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category_id == category_id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products