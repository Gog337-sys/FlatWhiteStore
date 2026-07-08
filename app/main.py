from fastapi import FastAPI
from app.api.health import router as health_router
from app.config.config import get_settings
from app.schemas.product import ProductCreate, ProductResponse
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(health_router)
@app.get("/")
def root():
    return {
    "message": f"{settings.app_name} is running",
    }

@app.get("/product", response_model=ProductResponse)
def create_product(product: ProductCreate):
    return {
        "id": 1,
        "price": product.price,
        "size": product.size,
        "name": product.name,
    }
@app.get("/hello")
def hello():
    return {
        "message": "Hello, FastAPI!",
    }

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
    }

@app.get("/search")
def search_items(query: str, limit: int = 10):
    return {
        "query": query,
        "limit": limit,
    }