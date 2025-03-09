from datetime import datetime

from sqlalchemy import Enum, String, text
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
    is_verified: Mapped[bool] = mapped_column(nullable=False, server_default=text("false"))

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False, server_default="USER")
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("NOW()"), onupdate=datetime.utcnow)
