from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.product import Product
from app.models.category import Category
from app.models.favorite import Favorite
from app.repositories.product_repository import ProductRepository
from app.repositories.favorite_repository import FavoriteRepository
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.db = db
        self.favorite_repo = FavoriteRepository(db)

    def create_product(self, schema: ProductCreate, current_user) -> Product:
        category_id = None
        if schema.category_name:
            category = self.db.query(Category).filter(Category.name == schema.category_name).first()
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category '{schema.category_name}' not found"
                )
            category_id = category.id

        product = Product(
            price=schema.price,
            size=schema.size,
            name=schema.name,
            category_id=category_id,
        )

        try:
            product = self.repository.create(product)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product with this name already exists"
            )

        if schema.is_favorite and current_user:
            favorite = Favorite(user_id=current_user.id, product_id=product.id)
            try:
                self.favorite_repo.create(favorite)
            except IntegrityError:
                pass

        return product

    def get_products(self, category_name: str | None = None, current_user = None, favorites_only: bool = False) -> list[Product]:
        user_id = current_user.id if current_user else None
        products = self.repository.get_all(
            category_name=category_name,
            user_id=user_id,
            favorites_only=favorites_only
        )

        if current_user:
            favorite_product_ids = {fav.product_id for fav in self.favorite_repo.get_all_by_user(current_user.id)}
            for product in products:
                product.is_favorite = product.id in favorite_product_ids
        else:
            for product in products:
                product.is_favorite = False

        return products

    def get_product(self, product_id: int, current_user = None) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if current_user:
            favorite = self.favorite_repo.get_by_user_and_product(current_user.id, product_id)
            product.is_favorite = favorite is not None
        else:
            product.is_favorite = False

        return product

    def update_product(self, product_id: int, schema: ProductUpdate) -> Product:
        product = self.get_product(product_id)

        update_data = schema.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided"
            )

        if 'category_name' in update_data:
            category_name = update_data.pop('category_name')
            if category_name is not None:
                category = self.db.query(Category).filter(Category.name == category_name).first()
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Category '{category_name}' not found"
                    )
                product.category_id = category.id
            else:
                product.category_id = None

        for field, value in update_data.items():
            setattr(product, field, value)

        return self.repository.update(product)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.repository.delete(product)