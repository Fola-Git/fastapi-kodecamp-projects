from fastapi import FastAPI
from .database import init_db
from .middleware import add_timing_header
from .cors import add_cors
from .routers import products, users, cart

app = FastAPI(title="E-Commerce API")
add_cors(app)
add_timing_header(app)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)
