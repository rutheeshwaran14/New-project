from sqlalchemy import Column, Integer, DateTime, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from website.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    total_amount = Column(DECIMAL(10, 2), nullable=False)

    status = Column(
        Enum("pending", "processing", "shipped", "delivered", "cancelled", name="order_status"),
        default="pending",
        nullable=False
    )

    payment_status = Column(
        Enum("pending", "paid", "failed", "refunded", name="payment_status"),
        default="pending",
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    # Optional: link to Payment (if you implement a Payment model)
    payment = relationship("Payment", back_populates="order", uselist=False)