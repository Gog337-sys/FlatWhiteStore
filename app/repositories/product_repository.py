from sqlalchemy.orm import Session
from typing import cast

from app.models.product import Product
from app.models.category import Category
from app.models.favorite import Favorite

class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        return self._upsert(product)

    def update(self, product: Product) -> Product:
        return self._upsert(product)

    def _upsert(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    def get_all(self, category_name: str | None = None, user_id: int | None = None, favorites_only: bool = False) -> list[Product]:
        query = self.db.query(Product)
        if category_name:

            category = self.db.query(Category).filter(Category.name == category_name).first()
            if category:
                query = query.filter(Product.category_id == category.id)
            else:
                return []

        if favorites_only and user_id is not None:
            subquery = self.db.query(Favorite.product_id).filter(Favorite.user_id).subquery()
            query = query.filter(Product.id.in_(subquery))

        return cast(list[Product], query.all())

    def get_by_id(
            self,
            product_id: int,
            ) -> Product | None:
        return  (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()