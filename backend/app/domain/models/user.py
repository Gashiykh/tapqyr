from datetime import datetime

from sqlalchemy import Enum, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base
from ..enums import RoleEnum


class User(Base):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    avatar: Mapped[str] = mapped_column(nullable=True)

    tg_username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, null=False)
