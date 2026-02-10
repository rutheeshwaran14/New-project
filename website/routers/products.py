from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from website.database import SessionLocal
from website.models import Product
from website.schemas.schemas import ProductCreate, ProductOut
from website.auth import get_current_user, admin_required
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/products", tags=["Products"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Create a new product (Admin only)
# -----------------------------
@router.post("/", response_model=ProductOut)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)  # only admin
):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# -----------------------------
# Get all products (any authenticated user)
# -----------------------------
@router.get("/", response_model=list[ProductOut])
def get_all_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # any logged-in user
):
    products = db.query(Product).all()
    return products

# -----------------------------
# Get product by ID (any authenticated user)
# -----------------------------
from fastapi_cache.decorator import cache

@router.get(
    "/{product_id}",
    response_model=ProductOut,
    operation_id="get_product_by_id"  # unique operation ID to avoid warning
)
@cache(expire=60)  # caches the response for 60 seconds
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a product by ID with caching.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# -----------------------------
# Update product (Admin only)
# -----------------------------
@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    updated: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)  # only admin
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated.name
    product.description = updated.description
    product.price = updated.price
    product.stock = updated.stock

    db.commit()
    db.refresh(product)
    return product

# -----------------------------
# Delete product (Admin only)
# -----------------------------
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)  # only admin
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

# Get all products
@router.get("/", response_model=list[ProductOut], operation_id="get_all_products")
@cache(expire=60)   # cache for 60 seconds
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Get single product
@router.get("/{product_id}", response_model=ProductOut, operation_id="get_product_by_id")
@cache(expire=120)  # cache for 120 seconds
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

