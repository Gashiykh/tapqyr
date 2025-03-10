from datetime import datetime
from pydantic import BaseModel

from app.domain.enums import RoleEnum


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    tg_username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    avatar: str | None = None
    role: RoleEnum = RoleEnum.USER
    is_verified: bool
    created_at: datetime
    updated_at: datetime