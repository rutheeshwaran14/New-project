from fastapi import FastAPI
from website.database import create_tables
from website.routers import products, orders, cart
from website.routers.auth import router as auth_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from website.routers import payment

app = FastAPI(title="E-Commerce API")

# ---------------- Startup ----------------

@app.on_event("startup")
def startup():
    create_tables()

# ---------------- Routers ----------------
app.include_router(auth_router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)

app.include_router(payment.router)

# ---------------- Root ----------------
@app.get("/")
def home():
    return {"message": "Welcome to E-Commerce API"}
