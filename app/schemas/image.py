from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    filename: str
    photo_path: str
    image_url: str
