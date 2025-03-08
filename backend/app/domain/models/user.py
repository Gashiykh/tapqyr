from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class User(Base):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    avatar: Mapped[str] = mapped_column(nullable=True)

    tg_username: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    role: Mapped[str] = mapped_column()
    date_joined: Mapped[datetime] = mapped_column(default=datetime.utcnow)
