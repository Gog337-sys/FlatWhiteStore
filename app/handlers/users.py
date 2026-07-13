from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter(tags=["users"])
profile_router = APIRouter(prefix="/profile", tags=["profile"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get(
    "/users/me",
    response_model=UserResponse,
)
def get_my_user(current_user: User = Depends(get_current_user),service: UserService = Depends(get_user_service),):
    return service.get_user_profile(current_user.id)


@router.get(
    "/admin/users",
    response_model=list[UserResponse],
)
def get_admin_users(
    current_user: User = Depends(require_role(UserRole.admin)),
    service: UserService = Depends(get_user_service),
):
    return service.get_users()

@router.get("/profile", response_model=UserResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):

    return service.get_user_profile(current_user.id)