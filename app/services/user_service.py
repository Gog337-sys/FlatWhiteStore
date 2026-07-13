from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.favorite_repository import FavoriteRepository
from app.schemas.product import ProductResponse
from app.schemas.user import UserResponse


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db

    def create_user(self, schema) -> User:
        # ... ваш существующий код ...
        pass

    def get_users(self) -> list[User]:
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def get_user_profile(self, user_id: int) -> dict:
        """
        Возвращает данные профиля пользователя с его избранными продуктами.
        """
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Получаем избранные продукты через FavoriteRepository
        favorite_repo = FavoriteRepository(self.db)
        favorite_products = favorite_repo.get_favorites_by_user(user_id)

        # Преобразуем продукты в схему ProductResponse
        products_data = [ProductResponse.model_validate(p) for p in favorite_products]

        # Формируем ответ
        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "favorites": products_data,
        }