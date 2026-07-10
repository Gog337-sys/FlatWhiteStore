from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    return service.create_product(product_data)

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    return service.get_product(product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    service = ProductService(db)

    return service.update_product(product_id, product_data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    service.delete_product(product_id)