from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.schemas.product import ProductResponse
from app.services.favorite_service import FavoriteService

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
)

@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
        payload: FavoriteCreate,
        db: Session = Depends(get_db),
        current_user: User =Depends(get_current_user),
):
    service = FavoriteService(db)
    favorite = service.add_favorite(current_user, payload.product_id)
    return favorite

@router.get("/", response_model=list[ProductResponse])
def get_favorite(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    service = FavoriteService(db)
    products = service.get_favorites(current_user)
    return products