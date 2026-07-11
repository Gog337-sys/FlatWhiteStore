from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, get_current_user_optional
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService
from app.models.user import User

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ProductService(db)
    return service.create_product(product_data, current_user)

@router.get("/", response_model=list[ProductResponse])
def get_products(
    category_name: str | None = None,
    favorites_only: bool = Query(False, description="Показать только избранные продукты"),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    service = ProductService(db)
    return service.get_products(
        category_name=category_name,
        current_user=current_user,
        favorites_only=favorites_only
    )

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional)
):
    service = ProductService(db)
    return service.get_product(product_id, current_user)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # опционально, если нужно проверять права
):
    service = ProductService(db)
    return service.update_product(product_id, product_data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ProductService(db)
    service.delete_product(product_id)