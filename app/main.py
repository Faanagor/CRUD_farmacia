from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1.endpoints import products

app = FastAPI()
app.include_router(products.router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    init_db()
