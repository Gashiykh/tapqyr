from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base


class Category(Base):
    __tablename__ = 'category'

    name: Mapped[str] = mapped_column()