import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .user import User
    from .color import Color


class Palette(Base):
    __tablename__ = "palettes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="palettes")

    colors: Mapped[list["Color"]] = relationship(
        back_populates="palette",
        cascade="all, delete-orphan",
    )
