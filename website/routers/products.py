from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func

from website.database import SessionLocal
from website.models.product import Product
from website.dependencies.auth import admin_required
from website.schemas.product import ProductUpdate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


# -------------------- DB Dependency --------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- GET ALL PRODUCTS + CATEGORY FILTER --------------------

@router.get("/", response_model=list[ProductOut])
def get_products(
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product).filter(Product.is_deleted == False)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    return query.all()


# -------------------- GET SINGLE PRODUCT --------------------

@router.get("/{product_id}", response_model=ProductOut)
def get_single_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# -------------------- UPDATE PRODUCT (ADMIN) --------------------

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(product, k, v)

    db.commit()
    db.refresh(product)

    return product


# -------------------- SOFT DELETE PRODUCT (ADMIN) --------------------

@router.delete("/{product_id}")
def soft_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_deleted = True
    product.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Product deleted successfully"}