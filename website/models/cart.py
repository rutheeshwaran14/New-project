from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from website.models.base import Base


class Cart(Base):
    __tablename__ = "carts"  # plural for consistency with other tables

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    user = relationship("User", backref="cart_items")
    product = relationship("Product")