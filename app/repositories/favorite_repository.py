from typing import cast

from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.models.product import Product
from app.test_repository import products


class FavoriteRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def delete(self, favorite: Favorite) -> Favorite:
        self.db.delete(favorite)
        self.db.commit()

    def get_user_and_product(self, user_id: int, product_id: int) -> Favorite | None:
        return (
            self.db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.product_id == product_id)
            .first()
        )

    def get_favorites_by_user(self, user_id: int) -> list[Product]:
        return cast(
            list[Product],
            self.db.query(Product)
            .join(Favorite, Favorite.product_id == Product.id)
            .filter(Favorite.user_id == user_id)
            .all()
        )