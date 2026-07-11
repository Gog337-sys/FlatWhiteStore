import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from app.handlers.health import router as health_router
from app.config.config import get_settings
from app.database import Base, engine
from app.handlers.auth import router as auth_router
from app.handlers.products import router as products_router
from app.handlers.favorites import router as favorites_router
from app.handlers.category import router as category_router
from app.handlers.users import router as users_router
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.models.favorite import Favorite

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(health_router)
app.include_router(category_router)
app.include_router(favorites_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)