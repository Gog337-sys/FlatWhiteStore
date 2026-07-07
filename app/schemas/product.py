from pydantic import BaseModel

class ProductCreate(BaseModel):
    price: int
    size: int
    name: str

class ProductResponse(BaseModel):
    id: int
    price: int
    size: int
    name: str