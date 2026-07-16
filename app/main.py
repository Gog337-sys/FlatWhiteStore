import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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
from app.handlers.users import profile_router
from app.handlers import images


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

MEDIA_DIR = Path(__file__).resolve().parent / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(health_router)
app.include_router(category_router)
app.include_router(favorites_router)
app.include_router(profile_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # порт Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/media",
    StaticFiles(directory=MEDIA_DIR),
    name="media",
)

app.include_router(images.router)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)