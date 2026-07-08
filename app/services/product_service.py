from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, schema: ProductCreate) -> Product:
        product = Product(
            price=schema.price,   # исправлено 'prise'
            size=schema.size,
            name=schema.name,
        )
        try:
            return self.repository.create(product)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with this name already exists"
            )

    def get_products(self) -> list[Product]:
        return self.repository.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product

    def update_product(self, product_id: int, schema: ProductUpdate) -> Product:
        product = self.get_product(product_id)

        update_data = schema.model_dump(exclude_unset=True)  # или .dict(exclude_unset=True) для Pydantic v1
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided"
            )

        for field, value in update_data.items():
            setattr(product, field, value)

        return self.repository.update(product)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.repository.delete(product)