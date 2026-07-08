from fastapi import FastAPI

from app.database import Base, engine
from app.handlers.products import router as products_router
from app.models.product import Product

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products_router)


@app.get("/")
def root():
    return {"message": "Hello World"}