from datetime import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User
from .post import Post


class Comment(Base):
    __tablename__ = 'comment'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    text: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=text("NOW()"))

    #Обратные связи
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )

    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )