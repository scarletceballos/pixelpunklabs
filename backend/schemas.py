from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    created_at: datetime

# Image schemas
class ImageGenerationRequest(BaseModel):
    prompt: str
    style: str = "steampunk"
    num_images: int = 1

class ImageBase(BaseModel):
    prompt: str
    user_id: str
    image_url: str

class ImageCreate(ImageBase):
    pass

class ImageInDB(ImageBase):
    id: str
    created_at: datetime

class ImageGenerationResponse(BaseModel):
    success: bool
    image_data: Optional[str]
    image_id: Optional[str]
    error: Optional[str]

# Asset Generation schemas
class GenerationRequest(BaseModel):
    prompt: str
    type: str = "image"  # "image" or "3d"
    style_preferences: Optional[dict] = None

class GenerationResponse(BaseModel):
    asset_url: str
    type: str
    prompt: str
    metadata: Optional[dict] = None 