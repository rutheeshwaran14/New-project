from sqlalchemy import Column, Integer, DateTime, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from website.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    total_amount = Column(DECIMAL(10, 2), nullable=False)

    status = Column(
        Enum("pending", "processing", "shipped", "delivered", "cancelled"),
        default="pending"
    )

    payment_status = Column(
        Enum("pending", "paid", "failed", "refunded"),
        default="pending"
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ THIS IS REQUIRED
    user = relationship("User", back_populates="orders")

    items = relationship("OrderItem", back_populates="order")
    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )
