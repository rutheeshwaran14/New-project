from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from website.database import get_db
from website.models.order import Order
from website.models.product import  Product
from website.models.user import  User
from website.schemas.schemas import OrderCreate, OrderOut
from website.auth import get_current_user , admin_required

router = APIRouter(prefix="/orders", tags=["Orders"])


# -----------------------------
# Create an order
# -----------------------------
@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if product exists
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check stock
    if order.quantity > product.stock:
        raise HTTPException(status_code=400, detail="Not enough stock available")
    
    # Reduce stock
    product.stock -= order.quantity
    
    # Create order
    new_order = Order(
        user_id=order.user_id,
        product_id=order.product_id,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return new_order

# -----------------------------
# Get all orders
# -----------------------------
@router.get("/", response_model=list[OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

# -----------------------------
# Get order by ID
# -----------------------------
@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# -----------------------------
# Delete an order
# -----------------------------
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Restore stock when order is deleted
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        product.stock += order.quantity
    
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}



@router.post("/", response_model=OrderOut)
def create_order(
    order: OrderCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # any logged-in user
):
    # Optional: ensure user_id matches token user
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create order for another user")
    
    # rest of code...
