from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    amount = Column(Float)
    status = Column(String(20))   # ✅ Make sure this exists

    product = relationship("Product")