from pydantic import BaseModel
from typing import Optional


class JewelryItem(BaseModel):
    id: str
    name: str
    type: str
    image: str
    description: Optional[str] = None


class TryOnRequest(BaseModel):
    jewelry_id: str


class TryOnResponse(BaseModel):
    image_url: str
    video_url: str
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
