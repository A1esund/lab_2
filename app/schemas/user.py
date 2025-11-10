from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    # description в вашей модели нет, убираем его

    class Config:
        from_attributes = True
