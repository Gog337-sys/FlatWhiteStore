from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):
    price: int = Field(ge=1500, le=9999)
    size: int = Field(ge=32, le=60)
    name: str = Field(min_length=1, max_length=200)

class ProductUpdate(BaseModel):
    price: int | None =Field(default=None, ge=1500, le=9999)
    size: int | None = Field(default=None, ge=32, le=60)
    name: str | None = Field(default=None, min_length=1, max_length=200)

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price: int
    size: int
    name: str