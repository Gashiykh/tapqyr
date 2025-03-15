from pydantic import (
    BaseModel,
    Field,
    field_validator
)
from fastapi import (
    HTTPException,
    status
)

from app.domain.enums import RoleEnum


class UserBase(BaseModel):
    username: str
    tg_username: str


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        description="Пароль должен содержать минимум 8 символов"
    )
    confirm_password: str

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password, values):
        password = values.data.get("password")
        if password and confirm_password != password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароли не совпадают"
            )
        return confirm_password

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data.pop("confirm_password", None)
        return data


class UserRead(UserBase):
    id: int
    avatar: str | None = None
    role: RoleEnum = RoleEnum.USER
    is_verified: bool