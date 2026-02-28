from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from website.models.base import Base
from sqlalchemy.orm import relationship

class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", lazy="joined")  # 🔥 IMPORTANT