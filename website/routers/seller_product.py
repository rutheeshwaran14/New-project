from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from website.database import get_db
from website.models.product import Product
from website.models.user import User  # must import User
from website.schemas.product import ProductCreate, ProductOut
from website.dependencies.auth import seller_required

router = APIRouter(prefix="/seller/products", tags=["Seller Products"])

@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    seller: User = Depends(seller_required)  # <-- consistent naming
):
    db_product = Product(**product.dict(), seller_id=seller.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[ProductOut])
def list_my_products(
    db: Session = Depends(get_db),
    seller: User = Depends(seller_required)  # <-- same here
):
    return db.query(Product).filter(Product.seller_id == seller.id).all()
