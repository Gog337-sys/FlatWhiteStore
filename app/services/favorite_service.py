from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from app.models.product import Product
from app.repositories.favorite_repository import FavoriteRepository
from app.schemas.favorite import FavoriteCreate

class FavoriteService:
    def __init__(self, db: Session):
        self.repository = FavoriteRepository(db)
        self.db = db

    def add_favorite(self, user_id: int, schema: FavoriteCreate) -> Favorite:
        # Проверка существования продукта
        product = self.db.query(Product).filter(Product.id == schema.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Проверка, не добавлен ли уже
        existing = self.repository.get_by_user_and_product(user_id, schema.product_id)
        if existing:
            raise HTTPException(status_code=409, detail="Product already in favorites")

        favorite = Favorite(user_id=user_id, product_id=schema.product_id)
        return self.repository.create(favorite)

    def remove_favorite(self, user_id: int, product_id: int) -> None:
        favorite = self.repository.get_by_user_and_product(user_id, product_id)
        if not favorite:
            raise HTTPException(status_code=404, detail="Favorite not found")
        self.repository.delete(favorite)

    def get_user_favorites(self, user_id: int) -> list[Favorite]:
        return self.repository.get_all_by_user(user_id)