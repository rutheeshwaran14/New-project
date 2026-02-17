from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from website.models.base import Base



class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)

    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(50), default="India")

    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")
