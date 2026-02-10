from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base

DATABASE_URL = "mysql+pymysql://root:Rutheesh$@localhost:3306/ecommerce"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    # Import all models here
    from website.models.user import User
    from website.models.product import Product
    from website.models.cart import Cart
    from website.models.order import Order

    Base.metadata.create_all(bind=engine, checkfirst=True)
