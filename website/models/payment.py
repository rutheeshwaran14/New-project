from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from website.models.base import Base



class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(Enum("card", "upi", "netbanking", "cod", "wallet"), nullable=False)

    status = Column(Enum("pending", "success", "failed", "refunded"), default="pending")
    transaction_id = Column(String(100), unique=True, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="payment", uselist=False)
