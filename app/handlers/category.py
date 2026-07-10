from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


def get_category_service(
    db: Session = Depends(get_db),
) -> CategoryService:
    return CategoryService(db)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    schema: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
):
    return service.create_category(schema)


@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def get_categories(
    service: CategoryService = Depends(get_category_service),
):
    return service.get_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
):
    return service.get_category(category_id)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    schema: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
):
    return service.update_category(category_id, schema)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> None:
    service.delete_category(category_id)