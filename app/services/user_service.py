from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.favorite_repository import FavoriteRepository
from app.schemas.product import ProductResponse
from app.schemas.user import UserResponse, UserCreate


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db

    def create_user(self, schema: UserCreate) -> User:
        existing_user = self.repository.get_by_email(schema.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        user = User(
            email=schema.email,
            hashed_password=hash_password(schema.password),
            name=schema.name,
            is_active=True,

        )
        return self.repository.create(user)

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

        user = self.repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        favorite_repo = FavoriteRepository(self.db)
        favorite_products = favorite_repo.get_favorites_by_user(user_id)

        products_data = [ProductResponse.model_validate(p) for p in favorite_products]

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "favorites": products_data,
        }