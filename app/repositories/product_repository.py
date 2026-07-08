from sqlalchemy.orm import Session

from app.models.product import Product


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

    def get_all(self) -> list[Product]:
        return self.db.query(Product).all()

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