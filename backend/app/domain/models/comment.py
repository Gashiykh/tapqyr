from datetime import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Comment(Base):
    __tablename__ = 'comment'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column()
