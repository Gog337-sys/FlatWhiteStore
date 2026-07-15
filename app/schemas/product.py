from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    price: int = Field(ge=1500, le=9999)
    size: int = Field(ge=32, le=60)
    name: str = Field(min_length=1, max_length=200)
    category_name: str | None = Field(default=None, min_length=1, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)
    is_favorite: bool | None = Field(default=False)

class ProductUpdate(BaseModel):
    price: int | None = Field(default=None, ge=1500, le=9999)
    size: int | None = Field(default=None, ge=32, le=60)
    name: str | None = Field(default=None, min_length=1, max_length=200)
    category_name: str | None = Field(default=None, min_length=1, max_length=100)

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price: int
    size: int
    name: str
    category_id: int | None
    is_favorite: bool = Field(default=False, description="Добавлен ли в избранное текущего пользователя")