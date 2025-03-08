from sqlalchemy import Enum
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base
from ..enums import BuildingsEnum


class Location(Base):
    __tablename__ = 'location'

    building: Mapped[BuildingsEnum] = mapped_column(Enum(BuildingsEnum), nullable=False)
    room: Mapped[int] = mapped_column()