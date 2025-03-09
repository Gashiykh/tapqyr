from datetime import datetime
from pydantic import BaseModel

from app.domain.enums import RoleEnum


class UserBase(BaseModel):
    username: str
    tg_username: str
    role: RoleEnum = RoleEnum.USER


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    avatar: str | None = None
    is_verified: bool
    created_at: datetime
    updated_at: datetime