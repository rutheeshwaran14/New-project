# website/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from website.database import engine, Base
from website.routers import (
    auth_router, users_router, products_router, orders_router,
    payments_router, cart_router, wishlist_router, reviews_router
)
from website.routers import category, seller_product, seller_orders, admin_users
from website.routers import google_auth, profile
from website.utils.init_admin import create_default_admin
from config import settings

# -------------------- DATABASE INIT --------------------
Base.metadata.create_all(bind=engine)

# -------------------- FASTAPI APP --------------------
app = FastAPI(
    title="E-Commerce Backend",
    version="1.0.0",
    description="Production Ready E-Commerce Backend API",
)

# -------------------- SESSION MIDDLEWARE --------------------
# ✅ Must come BEFORE CORS middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="ecom_session",
    same_site="lax",    # Important for OAuth state
    https_only=False,   # localhost
    max_age=3600
)

# -------------------- CORS MIDDLEWARE --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React frontend
        "http://localhost:9007"   # backend (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# -------------------- ROOT ROUTE --------------------
@app.get("/")
def home():
    return {"message": "E-Commerce Backend Running"}

# -------------------- STARTUP EVENT --------------------
@app.on_event("startup")
def startup():
    create_default_admin()

# -------------------- INCLUDE ROUTERS --------------------
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(google_auth.router)
app.include_router(profile.router)
app.include_router(category.router)
app.include_router(seller_product.router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(reviews_router)
app.include_router(seller_orders.router)
app.include_router(admin_users.router)