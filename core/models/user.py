import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(32))
    login: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String)
