from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship
)

from .base import Base
if TYPE_CHECKING:
    from .post import Post


class Category(Base):
    __tablename__ = 'category'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    #Обратные связи
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="category",
        cascade="all, delete-orphan",
    )