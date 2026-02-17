from fastapi import FastAPI
from website.database import engine, Base
from website.routers import (
    auth_router,
    users_router,
    products_router,
    orders_router,
    payments_router,
    cart_router,
    wishlist_router,
    reviews_router
)
from website.routers import category
from website.routers import seller_product, seller_orders, admin_users
from website.utils.init_admin import create_default_admin


# -------------------- DB INIT --------------------

Base.metadata.create_all(bind=engine)


# -------------------- APP INIT --------------------

app = FastAPI(
    title="E-Commerce Backend",
    version="1.0.0",
    description="Production Ready E-Commerce Backend API"
)


# -------------------- STARTUP EVENTS --------------------

@app.on_event("startup")
def startup():
    create_default_admin()


# -------------------- AUTH & USER --------------------
app.include_router(auth_router)
app.include_router(users_router)


# -------------------- CATEGORY --------------------
app.include_router(category.router)


# -------------------- SELLER MODULE --------------------
app.include_router(seller_product.router)


# -------------------- PRODUCTS --------------------
app.include_router(products_router)


# -------------------- SHOPPING FLOW --------------------
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(orders_router)
app.include_router(payments_router)


# -------------------- UX --------------------
app.include_router(reviews_router)


# -------------------- SELLER ORDERS --------------------
app.include_router(seller_orders.router)


# -------------------- ADMIN PANEL --------------------
app.include_router(admin_users.router)
