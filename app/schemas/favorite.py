from pydantic import BaseModel
from app.schemas.product import ProductResponse

class FavoriteCreate(BaseModel):
    product_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    product: ProductResponse | None = None
    model_config = {"from_attributes": True}