from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProductCreate(BaseModel):
    price: int = Field(ge=1500, le=9999)
    size: int = Field(ge=32, le=60)
    name: str = Field(min_length=1, max_length=200)
    category_name: str | None = Field(default=None, min_length=1, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)
    is_favorite: bool | None = Field(default=False)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[int] = Field(None, ge=1500, le=9999)
    size: Optional[int] = Field(None, ge=32, le=60)
    category_name: Optional[str] = Field(None, min_length=1, max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    size: int
    category_name: str | None = None
    image_url: str | None = None
    description: str | None = None
    is_favorite: bool = Field(default=False, description="Добавлен ли в избранное текущего пользователя")