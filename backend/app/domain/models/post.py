from datetime import datetime
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base


class Post(Base):
    __tablename__ = 'post'

    author_id: Mapped[int] = mapped_column()

    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()
    is_resolved: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()

    location_id: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column()