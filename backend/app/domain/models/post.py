from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    String,
    text,
    Enum,
    Boolean
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship
)

from ..enums import StatusPostEnum
from .base import Base
if TYPE_CHECKING:
    from .category import Category
    from .comment import Comment



class Post(Base):
    __tablename__ = 'post'

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    status: Mapped[StatusPostEnum] = mapped_column(Enum(StatusPostEnum), nullable=False)

    photo: Mapped[str] = mapped_column(String, nullable=True)

    is_resolved: Mapped[bool] = mapped_column(Boolean, nullable=True, server_default=text("false"))

    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("NOW()"), onupdate=datetime.utcnow)


    location_id: Mapped[int] = mapped_column(ForeignKey('location.id', ondelete="SET NULL"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete="SET NULL"), nullable=False)

    #Обратные связи
    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    location: Mapped["Location"] = relationship(
        "Location",
        back_populates="posts",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="posts"
    )

    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )