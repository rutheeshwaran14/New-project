from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models.product import Product
from website.dependencies.auth import admin_required
from datetime import datetime
from website.schemas.product import ProductUpdate


router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔴 ADMIN SOFT DELETE PRODUCT
@router.delete("/{product_id}")
def soft_delete_product(product_id: int,
                        db: Session = Depends(get_db),
                        admin=Depends(admin_required)):

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    product.is_deleted = True
    product.deleted_at = datetime.utcnow()

    db.commit()

    return {"message": "Product soft deleted successfully"}

@router.put("/{product_id}")
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    admin = Depends(admin_required)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(product, k, v)

    db.commit()
    return product
