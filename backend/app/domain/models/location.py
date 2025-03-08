from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base


class Location(Base):
    __tablename__ = 'location'

    building: Mapped[str] = mapped_column()
    room: Mapped[int] = mapped_column()