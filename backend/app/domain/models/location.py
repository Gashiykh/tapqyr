from sqlalchemy import Enum, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship
)

from ..enums import BuildingsEnum

from .base import Base
from .post import Post


class Location(Base):
    __tablename__ = 'location'

    building: Mapped[BuildingsEnum] = mapped_column(Enum(BuildingsEnum), nullable=False)
    room: Mapped[int] = mapped_column(Integer, nullable=True)

    #Обратные связи
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="location",
        cascade="all, delete-orphan",
    )