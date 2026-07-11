from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    product_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    product_id: int

    class Config:
        from_attributes = True