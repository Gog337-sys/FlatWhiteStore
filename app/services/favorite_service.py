from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.models.product import Product
from app.models.user import User
from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.product_repository import ProductRepository

class FavoriteService:

    def __init__(self, db: Session):
        self.repository = FavoriteRepository(db)
        self.product_repo = ProductRepository(db)

    def add_favorite(self, user: User, product_id: int) -> Favorite:
        # Проверяем, существует ли продукт
        product = self.product_repo.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Проверяем, не добавлен ли уже в избранное
        existing = self.repository.get_user_and_product(user.id, product_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already in favorites"
            )

    def remove_favorite(self, user: User, product_id: int) -> None:
        favorite = self.repository.get_user_and_product(user.id, product_id)
        if favorite is None:
            raise  HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        self.repository.delete(favorite)

    def get_favorites(self, user: User) -> list[Product]:
        return self.repository.get_favorites_by_user(user.id)
