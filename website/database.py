from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from website.models.base import Base

DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from website.models.user import User
    from website.models.product import Product
    from website.models.cart import Cart
    from website.models.order import Order

    
