import datetime
import uuid

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: str
    phone_number: str
    first_name: str
    last_name: str
    photo: str


class UserCreate(UserBase):
    email: EmailStr
    password: str
    password_confirm: str


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserInDB(UserBase):
    hashed_password: str