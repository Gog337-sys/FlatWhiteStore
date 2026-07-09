from pydantic import BaseModel

class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    user_id: int
